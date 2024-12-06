import numpy as np
import xarray as xr


def add_conversion(
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

    # Operation - Conversion

    operation_conversion_power_capacity = m.add_variables(
        name="operation_conversion_power_capacity",
        lower=0,
        coords=[p.area, p.conversion_tech, p.year_op],
    )

    operation_conversion_power = m.add_variables(
        name="operation_conversion_power",
        lower=0,
        coords=[p.area, p.conversion_tech, p.hour, p.year_op],
    )

    # Operation - Conversion intermediate variables

    operation_conversion_net_generation = m.add_variables(
        name="operation_conversion_net_generation",
        coords=[p.area, p.conversion_tech, p.hour, p.resource, p.year_op],
        mask=np.isfinite(p.conversion_factor) * (p.conversion_factor != 0),
    )

    # Planning - Conversion

    planning_conversion_power_capacity = m.add_variables(
        name="planning_conversion_power_capacity",
        lower=0,
        coords=[p.area, p.conversion_tech, p.year_dec, p.year_inv],
        mask=xr.where(
            cond=p.conversion_early_decommissioning,
            x=(p.year_inv < p.year_dec)
            * (p.year_dec <= p.conversion_end_of_life)
            * np.logical_or(
                p.year_dec <= p.year_inv.max(),
                p.year_dec == p.conversion_end_of_life,
            ),
            y=p.year_dec == p.conversion_end_of_life,
        ),
    )

    # Costs - Conversion

    operation_conversion_costs = m.add_variables(
        name="operation_conversion_costs", coords=[p.area, p.conversion_tech, p.year_op]
    )

    planning_conversion_costs = m.add_variables(
        name="planning_conversion_costs", coords=[p.area, p.conversion_tech, p.year_op]
    )

    # ------------------
    # Objective function
    # ------------------

    annualised_totex_def.lhs += operation_conversion_costs.sum(
        "conversion_tech"
    ) + planning_conversion_costs.sum("conversion_tech")

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint.lhs += operation_conversion_net_generation.sum("conversion_tech")

    # Operation - Conversion

    m.add_constraints(
        operation_conversion_power
        - operation_conversion_power_capacity
        * xr.where(
            cond=p.conversion_tech.isin(
                p.conversion_availability.dropna(dim="conversion_tech").conversion_tech
            ),
            x=p.conversion_availability,
            y=1,
        )
        <= 0,
        name="operation_conversion_power_max_constraint",
    )

    m.add_constraints(
        operation_conversion_power - operation_conversion_power_capacity * p.conversion_availability
        == 0,
        name="operation_conversion_must_run_constraint_equality",
        mask=p.conversion_must_run == 1,
    )

    m.add_constraints(
        operation_conversion_power
        - operation_conversion_power_capacity
        * xr.where(
            np.isfinite(p.conversion_availability),
            p.conversion_availability,
            1,
        )
        * p.conversion_must_run
        >= 0,
        name="operation_conversion_must_run_constraint_inequality",
        mask=(0 < p.conversion_must_run) * (p.conversion_must_run < 1),
    )

    # Operation - Conversion unit commitment

    m.add_constraints(
        -p.conversion_ramp_up * operation_conversion_power_capacity * time_step
        + operation_conversion_power
        - operation_conversion_power.shift(hour=1)
        <= 0,
        name="operation_conversion_ramp_up_constraint",
        mask=np.isfinite(p.conversion_ramp_up) * (p.hour != p.hour[0]),
    )

    m.add_constraints(
        -p.conversion_ramp_down * operation_conversion_power_capacity * time_step
        + operation_conversion_power.shift(hour=1)
        - operation_conversion_power
        <= 0,
        name="operation_conversion_ramp_down_constraint",
        mask=np.isfinite(p.conversion_ramp_down) * (p.hour != p.hour[0]),
    )

    # TODO: Ramp constraints fo lag > 1 not implemented yet and for storage also

    # Operation - Conversion other constraints

    m.add_constraints(
        time_step * operation_conversion_power.sum(["hour"]) <= p.conversion_max_yearly_production,
        name="operation_conversion_yearly_production_max_constraint",
        mask=np.isfinite(p.conversion_max_yearly_production),
    )

    m.add_constraints(
        operation_conversion_power_capacity <= p.conversion_power_capacity_max,
        name="operation_conversion_power_capacity_max_constraint",
        mask=np.isfinite(p.conversion_power_capacity_max),
    )

    m.add_constraints(
        operation_conversion_power_capacity >= p.conversion_power_capacity_min,
        name="operation_conversion_power_capacity_min_constraint",
        mask=np.isfinite(p.conversion_power_capacity_min),
    )

    # Operation - Conversion intermediate variables

    m.add_constraints(
        -operation_conversion_power_capacity
        + planning_conversion_power_capacity.where(
            (p.year_inv <= p.year_op) * (p.year_op < p.year_dec)
        ).sum(["year_dec", "year_inv"])
        == 0,
        name="operation_conversion_power_capacity_def",
    )

    m.add_constraints(
        -operation_conversion_net_generation
        + time_step * (p.conversion_factor * operation_conversion_power)
        == 0,
        name="operation_conversion_net_generation_def",
        mask=np.isfinite(p.conversion_factor) * (p.conversion_factor != 0),
    )

    # Planning - Conversion

    m.add_constraints(
        planning_conversion_power_capacity.sum("year_dec")
        <= p.conversion_power_capacity_investment_max,
        name="planning_conversion_power_capacity_max_constraint",
        mask=np.isfinite(p.conversion_power_capacity_investment_max)
        * np.not_equal(
            p.conversion_power_capacity_investment_max, p.conversion_power_capacity_investment_min
        ),
    )

    m.add_constraints(
        planning_conversion_power_capacity.sum("year_dec")
        >= p.conversion_power_capacity_investment_min,
        name="planning_conversion_power_capacity_min_constraint",
        mask=np.isfinite(p.conversion_power_capacity_investment_min)
        * np.not_equal(
            p.conversion_power_capacity_investment_max, p.conversion_power_capacity_investment_min
        ),
    )

    m.add_constraints(
        planning_conversion_power_capacity.sum("year_dec")
        == p.conversion_power_capacity_investment_min,
        name="planning_conversion_power_capacity_def",
        mask=np.isfinite(p.conversion_power_capacity_investment_min)
        * np.equal(
            p.conversion_power_capacity_investment_max, p.conversion_power_capacity_investment_min
        ),
    )

    # Costs - Conversion

    m.add_constraints(
        -operation_conversion_costs
        + (p.conversion_variable_cost * operation_conversion_power.sum("hour"))
        + (p.conversion_fixed_cost * operation_conversion_power_capacity)
        == 0,
        name="operation_conversion_costs_def",
    )

    m.add_constraints(
        -planning_conversion_costs
        + (
            (planning_conversion_power_capacity * p.conversion_annuity_cost)
            .where((p.year_inv <= p.year_op) * (p.year_op < p.year_dec))
            .sum(["year_dec", "year_inv"])
        ).where(
            cond=p.conversion_annuity_perfect_foresight,
            other=(
                (
                    planning_conversion_power_capacity.sum("year_dec")
                    * p.conversion_annuity_cost.min(
                        [dim for dim in p.conversion_annuity_cost.dims if dim == "year_dec"]
                    )
                )
                .where((p.year_inv <= p.year_op) * (p.year_op < p.conversion_end_of_life))
                .sum(["year_inv"])
            ),
        )
        == 0,
        name="planning_conversion_costs_def",
    )

    return m
