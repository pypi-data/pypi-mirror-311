import xarray as xr
from numpy.testing import assert_equal

from pommes.io.build_input_dataset import build_input_parameters, check_inputs, read_config_file


def test_build_from_test_conf(parameters):
    study = "test_case"
    config_ = read_config_file(study=study)

    p = build_input_parameters(config_)
    p = check_inputs(p)

    assert_equal(sorted([x for x in p.coords]), sorted([x for x in parameters.coords]))
    for coord in parameters.coords:
        coord1, coord2 = xr.broadcast(
            p[coord], parameters[coord]
        )  # Here coord converted to DataArray
        xr.testing.assert_equal(coord1, coord2)

    assert_equal(sorted([x for x in p.data_vars]), sorted([x for x in parameters.data_vars]))

    for variable in parameters.data_vars:
        da1, da2 = xr.broadcast(p[variable], parameters[variable])
        # print(variable)
        xr.testing.assert_equal(da1, da2)


def test_build_from_test_conf_default(parameters):
    study = "test_case"
    config_ = read_config_file(study=study)

    p = build_input_parameters(config_)
    p = p.drop_vars(["discount_factor", "discount_rate"])

    p = check_inputs(p)

    assert_equal(sorted([x for x in p.data_vars]), sorted([x for x in parameters.data_vars]))
