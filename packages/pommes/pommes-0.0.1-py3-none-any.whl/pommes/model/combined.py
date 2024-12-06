import numpy as np
import xarray as xr


def add_combined(
    model,
    model_parameters,
    annualised_totex_def,
    time_step,
    operation_adequacy_constraint,
):
    m = model
    p = model_parameters

    # ------------
    # Variables
    # ------------

    # Operation - Combined

    operation_combined_power_capacity = m.add_variables(
        name="operation_combined_power_capacity",
        lower=0,
        coords=[p.area, p.combined_tech, p.year_op],
    )

    operation_combined_power = m.add_variables(
        name="operation_combined_power",
        lower=0,
        coords=[p.area, p.combined_tech, p.mode, p.hour, p.year_op],
    )

    # Operation - Combined intermediate variables

    operation_combined_net_generation = m.add_variables(
        name="operation_combined_net_generation",
        coords=[p.area, p.combined_tech, p.hour, p.resource, p.year_op],
        mask=(np.isfinite(p.combined_factor) * (p.combined_factor != 0)).any(
            [dim for dim in ["mode"] if dim in p.combined_factor.dims]
        ),
    )

    # Planning - Combined

    planning_combined_power_capacity = m.add_variables(
        name="planning_combined_power_capacity",
        lower=0,
        coords=[p.area, p.combined_tech, p.year_dec, p.year_inv],
        mask=xr.where(
            cond=p.combined_early_decommissioning,
            x=(p.year_inv < p.year_dec)
            * (p.year_dec <= p.combined_end_of_life)
            * np.logical_or(
                p.year_dec <= p.year_inv.max(),
                p.year_dec == p.combined_end_of_life,
            ),
            y=p.year_dec == p.combined_end_of_life,
        ),
    )

    # Costs - Combined

    operation_combined_costs = m.add_variables(
        name="operation_combined_costs", coords=[p.area, p.combined_tech, p.year_op]
    )

    planning_combined_costs = m.add_variables(
        name="planning_combined_costs", coords=[p.area, p.combined_tech, p.year_op]
    )

    # ------------------
    # Objective function
    # ------------------

    annualised_totex_def.lhs += operation_combined_costs.sum(
        "combined_tech"
    ) + planning_combined_costs.sum("combined_tech")

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint.lhs += operation_combined_net_generation.sum("combined_tech")

    # Operation - Combined

    m.add_constraints(
        operation_combined_power.sum("mode") - operation_combined_power_capacity <= 0,
        name="operation_combined_power_max_constraint",
    )
    # TODO: must run in combined
    # m.add_constraints(
    #     operation_combined_power - operation_combined_power_capacity * p.combined_must_run
    #     == 0,
    #     name="operation_combined_must_run_constraint_equality",
    #     mask=(p.combined_must_run.sum("mode") == 1),
    # )
    #
    # m.add_constraints(
    #     operation_combined_power - operation_combined_power_capacity * p.combined_must_run >= 0,
    #     name="operation_combined_must_run_constraint_inequality",
    #     mask=(0 < p.combined_must_run) * (p.combined_must_run < 1),
    # )

    # Operation - Combined unit commitment

    # TODO: ramps in combined
    # m.add_constraints(
    #     -p.combined_ramp_up * m.variables.operation_combined_power_capacity * time_step
    #     + operation_combined_power
    #     - operation_combined_power.shift(hour=1)
    #     <= 0,
    #     name="operation_combined_ramp_up_constraint",
    #     mask=np.isfinite(p.combined_ramp_up) * (p.hour != p.hour[0]),
    # )
    #
    # m.add_constraints(
    #     -p.combined_ramp_down * m.variables.operation_combined_power_capacity * time_step
    #     + operation_combined_power.shift(hour=1)
    #     - operation_combined_power
    #     <= 0,
    #     name="operation_combined_ramp_down_constraint",
    #     mask=np.isfinite(p.combined_ramp_down) * (p.hour != p.hour[0]),
    # )
    #
    # # TODO: Ramp constraints fo lag > 1 not implemented yet and for storage also

    # Operation - Combined intermediate variables

    m.add_constraints(
        -operation_combined_power_capacity
        + planning_combined_power_capacity.where(
            (p.year_inv <= p.year_op) * (p.year_op < p.year_dec)
        ).sum(["year_dec", "year_inv"])
        == 0,
        name="operation_combined_power_capacity_def",
    )

    m.add_constraints(
        -operation_combined_net_generation
        + time_step * (p.combined_factor * operation_combined_power).sum(["mode"])
        == 0,
        name="operation_combined_net_generation_def",
        mask=(np.isfinite(p.combined_factor) * (p.combined_factor != 0)).any(
            [dim for dim in ["mode"] if dim in p.combined_factor.dims]
        ),
    )

    # Planning - Combined

    m.add_constraints(
        planning_combined_power_capacity.sum("year_dec")
        <= p.combined_power_capacity_investment_max,
        name="planning_combined_power_capacity_max_constraint",
        mask=np.isfinite(p.combined_power_capacity_investment_max)
        * np.not_equal(
            p.combined_power_capacity_investment_max, p.combined_power_capacity_investment_min
        ),
    )

    m.add_constraints(
        planning_combined_power_capacity.sum("year_dec")
        >= p.combined_power_capacity_investment_min,
        name="planning_combined_power_capacity_min_constraint",
        mask=np.isfinite(p.combined_power_capacity_investment_min)
        * np.not_equal(
            p.combined_power_capacity_investment_max, p.combined_power_capacity_investment_min
        ),
    )

    m.add_constraints(
        planning_combined_power_capacity.sum("year_dec")
        == p.combined_power_capacity_investment_min,
        name="planning_combined_power_capacity_def",
        mask=np.isfinite(p.combined_power_capacity_investment_min)
        * np.equal(
            p.combined_power_capacity_investment_max, p.combined_power_capacity_investment_min
        ),
    )

    # Costs - Combined

    m.add_constraints(
        -operation_combined_costs
        + (p.combined_variable_cost * operation_combined_power.sum("hour")).sum("mode")
        + p.combined_fixed_cost * operation_combined_power_capacity
        == 0,
        name="operation_combined_costs_def",
    )

    m.add_constraints(
        -planning_combined_costs
        + (
            (planning_combined_power_capacity * p.combined_annuity_cost)
            .where((p.year_inv <= p.year_op) * (p.year_op < p.year_dec))
            .sum(["year_dec", "year_inv"])
        ).where(
            cond=p.combined_annuity_perfect_foresight,
            other=(
                (
                    planning_combined_power_capacity.sum("year_dec")
                    * p.combined_annuity_cost.min(
                        [dim for dim in p.combined_annuity_cost.dims if dim == "year_dec"]
                    )
                )
                .where((p.year_inv <= p.year_op) * (p.year_op < p.combined_end_of_life))
                .sum(["year_inv"])
            ),
        )
        == 0,
        name="planning_combined_costs_def",
    )

    return m
