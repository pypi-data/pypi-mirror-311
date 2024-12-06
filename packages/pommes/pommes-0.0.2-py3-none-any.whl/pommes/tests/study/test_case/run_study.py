from pommes.common_plots import plot_capacities, plot_energy_balance, plot_power, plot_stock_level
from pommes.io.build_input_dataset import build_input_parameters, check_inputs, read_config_file
from pommes.io.save_solution import save_solution
from pommes.model.build_model import build_model

if __name__ == "__main__":
    study = "test_case"
    scenario = "ref"
    suffix = "_02161113"

    output_folder = f"study/{study}/output/{scenario}{suffix}"
    solver = "highs"  # ["gurobi", "xpress", "highs", "mosek"]

    config = read_config_file(study=study)

    model_parameters = build_input_parameters(config)
    model_parameters = check_inputs(model_parameters)
    model = build_model(model_parameters)

    model.solve(solver_name=solver)

    save_solution(
        model=model,
        output_folder=output_folder,
        model_parameters=model_parameters,
    )

    area = "area_1"

    plot_power(
        model_solution=model.solution,
        plot_folder=f"{output_folder}/plots",
        plot_name="power",
    )

    plot_energy_balance(
        model_parameters=model_parameters,
        model_solution=model.solution.sel(year_op=2030, drop=True),
        facet_row="resource",
        facet_col="area",
        plot_folder=f"{output_folder}/plots",
        plot_name="energy_balance",
    )

    plot_capacities(
        model_parameters=model_parameters,
        model_solution=model.solution,
        plot_folder=f"{output_folder}/plots",
        area=area,
        plot_name="installed_capacities",
    )

    plot_stock_level(
        model_parameters=model_parameters,
        model_solution=model.solution,
        plot_folder=f"{output_folder}/plots",
        area=area,
        plot_name="stock_level",
    )
