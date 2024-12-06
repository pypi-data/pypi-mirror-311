import numpy as np
from linopy import Model

from pommes.model.carbon import add_carbon
from pommes.model.combined import add_combined
from pommes.model.conversion import add_conversion
from pommes.model.net_import import add_net_import
from pommes.model.storage import add_storage
from pommes.model.transport import add_transport
from pommes.model.turpe import add_turpe


def build_model(model_parameters):
    """
    Build a Linopy Model based on the provided model parameters.

    Parameters
    ----------
    model_parameters : xarray Dataset
        Model parameters containing information about the energy system, including areas, years_op,
        invest years_op, hours, resources, conversion technologies, storage, repurposing, demand,
        net imports, carbon, and turpe.

    Returns
    -------
    Model
        Linopy Model object representing the energy system model.

    Notes
    -----
    This function builds a Linopy Model by specifying variables, objectives, and constraints based
    on the provided model parameters. The resulting model can be used for optimization and
    analysis of the energy system.
    """
    p = model_parameters

    time_step = 1.0
    if len(p.hour) > 1:
        time_step = p.hour.values[1] - p.hour.values[0]

    m = Model()

    # ------------
    # Variables
    # ------------

    # Operation - load_shedding & spillage

    operation_load_shedding = m.add_variables(
        name="operation_load_shedding",
        lower=0,
        mask=np.logical_or(
            np.isnan(p.load_shedding_max_capacity),
            p.load_shedding_max_capacity > 0,
        ),
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    operation_spillage = m.add_variables(
        name="operation_spillage",
        lower=0,
        mask=np.logical_or(
            np.isnan(p.spillage_max_capacity),
            p.spillage_max_capacity > 0,
        ),
        coords=[p.area, p.hour, p.resource, p.year_op],
    )

    # Costs - load_shedding & spillage

    operation_load_shedding_costs = m.add_variables(
        name="operation_load_shedding_costs",
        coords=[p.area, p.year_op],
    )

    operation_spillage_costs = m.add_variables(
        name="operation_spillage_costs",
        coords=[p.area, p.year_op],
    )

    # Annualised costs

    annualised_totex = m.add_variables(name="annualised_totex", coords=[p.area, p.year_op])

    # ------------------
    # Objective function
    # ------------------

    m.add_objective(p.discount_factor * annualised_totex.sum("area"))

    # --------------
    # Constraints
    # --------------

    # Adequacy constraint

    operation_adequacy_constraint = m.add_constraints(
        operation_load_shedding - operation_spillage - p.demand == 0,
        name="operation_adequacy_constraint",
    )

    # Operation - load_shedding & spillage

    m.add_constraints(
        operation_load_shedding <= p.load_shedding_max_capacity,
        mask=np.isfinite(p.load_shedding_max_capacity) * (p.load_shedding_max_capacity > 0),
        name="operation_load_shedding_max_constraint",
    )

    m.add_constraints(
        operation_spillage <= p.spillage_max_capacity,
        mask=np.isfinite(p.spillage_max_capacity) * (p.spillage_max_capacity > 0),
        name="operation_spillage_max_constraint",
    )

    # Costs - load_shedding & spillage

    m.add_constraints(
        -operation_load_shedding_costs
        + (operation_load_shedding.sum(["hour"]) * p.load_shedding_cost).sum(["resource"])
        == 0,
        name="operation_load_shedding_costs_def",
    )

    m.add_constraints(
        -operation_spillage_costs
        + (operation_spillage.sum(["hour"]) * p.spillage_cost).sum(["resource"])
        == 0,
        name="operation_spillage_costs_def",
    )
    # Annualised costs

    annualised_totex_def = m.add_constraints(
        -annualised_totex + operation_load_shedding_costs + operation_spillage_costs == 0,
        name="annualised_totex_def",
    )

    # -----------------------------------------
    # Other sets of variables and constraints
    # -----------------------------------------

    if "conversion" in p.keys() and p.conversion:
        m = add_conversion(m, p, annualised_totex_def, time_step, operation_adequacy_constraint)

    if "storage" in p.keys() and p.storage:
        m = add_storage(m, p, annualised_totex_def, time_step, operation_adequacy_constraint)

    if "transport" in p.keys() and p.transport:
        m = add_transport(m, p, annualised_totex_def, time_step, operation_adequacy_constraint)

    if "combined" in p.keys() and p.conversion:
        m = add_combined(m, p, annualised_totex_def, time_step, operation_adequacy_constraint)

    # if p.repurposing is not None:
    #     m = add_repurposing(m, p, annualised_totex_def, operation_adequacy_constraint)

    if "net_import" in p.keys() and p.net_import:
        m = add_net_import(m, p, annualised_totex_def, operation_adequacy_constraint)

    if "carbon" in p.keys() and p.carbon:
        m = add_carbon(m, p, annualised_totex_def, time_step)

    if "turpe" in p.keys() and p.turpe:
        m = add_turpe(m, p, annualised_totex_def)

    return m
