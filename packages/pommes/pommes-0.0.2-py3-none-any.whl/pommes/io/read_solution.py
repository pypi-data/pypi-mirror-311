import os

import pandas as pd
import xarray as xr


def read_csv_files(directory, index=False):
    """
    Read CSV files from a directory and return a dictionary of DataFrames.

    Parameters
    ----------
    directory : str
        The path to the directory containing CSV files.
    index : bool, optional
        Whether to set the first column as the index. Default is False.

    Returns
    -------
    dict
        A dictionary where keys are DataFrame names and values are DataFrames read from CSV files.
    """
    files = os.listdir(directory)

    csv_files = [file for file in files if file.endswith(".csv")]

    dataframes = {}

    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        dataframe_name = os.path.splitext(csv_file)[0]

        df = pd.read_csv(file_path, sep=";")

        if len(df.columns) > 2:
            if index:
                df.drop(columns=df.columns[0], inplace=True)

            df.set_index(df.columns[:-1].tolist(), inplace=True)

        dataframes[dataframe_name] = df

    return dataframes


def read_solution(directory_variables_path, index=False):
    """
    Read CSV files from variables directory and return merged xarray DataArrays.

    Parameters
    ----------
    directory_variables_path : str
        The path to the directory containing CSV files for variables.
    index : bool, optional
        Whether to set the first column as the index. Default is False.

    Returns
    -------
    xr.DataArray
        Merged xarray DataArray for variables.
    """
    dfs_var = read_csv_files(directory_variables_path, index=index)
    s = xr.merge([df.to_xarray() for df in dfs_var.values()])
    return s


def read_dual(directory_constraints_path, index=False):
    """
    Read CSV files from constraints directory and return merged xarray DataArrays.

    Parameters
    ----------
    directory_constraints_path : str
        The path to the directory containing CSV files for constraints.
    index : bool, optional
        Whether to set the first column as the index. Default is False.

    Returns
    -------
    xr.DataArray
        Merged xarray DataArray for constraints.
    """
    dfs_cons = read_csv_files(directory_constraints_path, index=index)
    d = xr.merge([df.to_xarray() for df in dfs_cons.values()])
    return d


import pandas as pd
from pathlib import Path


def generate_summary_dataframes_from_results(study_results):
    """
    Generate dataframes based on the data from the study results.

    Parameters:
    study_results (Path): Path to the directory containing the study results CSV files.

    Returns:
    dict: A dictionary of pandas DataFrames, each representing a different aspect of the study results.
    """
    dataframes = {}

    # Look for the computed countries
    path_totex = study_results / "annualised_totex.csv"
    totex = pd.read_csv(path_totex, sep=";", decimal=".")
    dataframes['Operation costs - EUR'] = totex
    countries = totex['area']

    # Processing demand
    # path_demand = f'{study_inputs}\demand.csv'
    # yearly_demand = pd.read_csv(path_demand, sep=";", decimal=".").groupby(['area', 'resource']).sum().drop(['hour'], axis=1)
    # yearly_demand = yearly_demand.loc[countries.to_numpy()].reset_index()
    # dataframes['Demand - MWh'] = yearly_demand

    path_capacity = study_results / "operation_conversion_capacity.csv"
    capacity = pd.read_csv(path_capacity, sep=";", decimal=".").groupby(['area', 'conversion_tech', 'year_op']).sum().drop(['year_inv'], axis=1)
    capacity = capacity.rename(columns={'operation_conversion_capacity': 'install_capacity'})
    capacity = capacity[capacity['install_capacity'] != 0].reset_index()
    dataframes['Production capacity - MW'] = capacity

    path_exchange = study_results / "operation_exchange_capacity.csv"
    exchange = pd.read_csv(path_exchange, sep=";", decimal=".").groupby(['area_from', 'area_to', 'exchange_tech', 'year_op']).sum().drop(['year_inv'], axis=1)
    exchange = exchange.rename(columns={'operation_exchange_capacity': 'exchange_capacity'})
    exchange = exchange[exchange['exchange_capacity'] != 0].reset_index()
    dataframes['Exchange capacity - MW'] = exchange

    path_storage_capacity = study_results / "operation_storage_power_capacity.csv"
    storage_capacity = pd.read_csv(path_storage_capacity, sep=";", decimal=".").groupby(['area', 'storage_tech', 'year_op']).sum().drop(['year_inv'], axis=1)
    storage_capacity = storage_capacity.rename(columns={'operation_storage_power_capacity': 'storage_power_capacity'})
    storage_capacity = storage_capacity[storage_capacity['storage_power_capacity'] != 0]
    path_storage_energy = study_results / "operation_storage_energy_capacity.csv"
    storage_energy = pd.read_csv(path_storage_energy, sep=";", decimal=".").groupby(['area', 'storage_tech', 'year_op']).sum().drop(['year_inv'], axis=1)
    storage_energy = storage_energy.rename(columns={'operation_storage_energy_capacity': 'storage_energy_capacity'})
    storage_energy = storage_energy[storage_energy['storage_energy_capacity'] != 0]
    storage = pd.merge(storage_capacity, storage_energy, on=['area', 'storage_tech', 'year_op'], how='outer').reset_index()
    dataframes['Storage capacity - MW-MWh'] = storage

    path_spillage = study_results / "operation_spillage.csv"
    yearly_spillage = pd.read_csv(path_spillage, sep=";", decimal=".").groupby(['area', 'resource', 'year_op']).sum().drop('hour', axis=1)
    yearly_spillage = yearly_spillage[yearly_spillage['operation_spillage'] != 0].reset_index()
    dataframes['Spillage - MWh'] = yearly_spillage

    path_curtailment = study_results / "operation_curtailment.csv"
    yearly_curtailment = pd.read_csv(path_curtailment, sep=";", decimal=".").groupby(['area', 'resource', 'year_op']).sum().drop('hour', axis=1)
    yearly_curtailment = yearly_curtailment[yearly_curtailment['operation_curtailment'] != 0].reset_index()
    dataframes['Loss of load - MWh'] = yearly_curtailment

    path_co2 = study_results / "operation_carbon_emissions.csv"
    yearly_co2 = pd.read_csv(path_co2, sep=";", decimal=".").groupby(['area', 'year_op']).sum().drop('hour', axis=1)
    yearly_co2 = yearly_co2[yearly_co2['operation_carbon_emissions'] != 0].reset_index()
    dataframes['CO2 emissions - tCO2eq'] = yearly_co2

    path_net_generation = study_results / "operation_conversion_net_generation.csv"
    yearly_net_generation = pd.read_csv(path_net_generation, sep=";", decimal=".").groupby(['area', 'conversion_tech', 'resource', 'year_op']).sum().drop('hour', axis=1)
    yearly_net_generation = yearly_net_generation[yearly_net_generation['operation_conversion_net_generation'] != 0].reset_index()
    dataframes['Production - MWh'] = yearly_net_generation

    path_net_imports_net_generation = study_results / "operation_net_import_net_generation.csv"
    yearly_net_imports = pd.read_csv(path_net_imports_net_generation, sep=";", decimal=".").groupby(['area', 'resource', 'year_op']).sum().drop('hour', axis=1)
    yearly_net_imports = yearly_net_imports[yearly_net_imports['operation_net_import_net_generation'] != 0].reset_index()
    dataframes['Net imports - MWh'] = yearly_net_imports

    return dataframes

def write_to_excel(dataframes, excel_file):
    """
    Write the dataframes to an Excel file.

    Parameters:
    dataframes (dict): A dictionary of pandas DataFrames to be written to the Excel file.
    excel_file (Path): Path to the Excel file where dataframes will be written.
    """
    with pd.ExcelWriter(excel_file.name) as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
