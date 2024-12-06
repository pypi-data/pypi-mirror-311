import numpy.testing as npt

import datatoolbox as dt


def test_register_units():
    dt.units.register_new_unit("persons = count")

    assert dt.units.is_valid_unit("persons")


def test_base_conversion1():
    # testing compound units and addtional units (CO2eq)
    hr_in_yr = dt.units.conversionFactor("yr", "h")

    try:
        npt.assert_almost_equal(
            hr_in_yr, 8765.812770749999
        )  # were counting leap years now?
    except Exception:
        npt.assert_almost_equal(
            hr_in_yr, 8766.0
        )  # allow for rounding (for some openscm versions)
    obs = dt.units.conversionFactor("Mt CO2eq / yr", "kg CO2eq / hr")
    exp = 1e9 / hr_in_yr
    npt.assert_almost_equal(obs, exp)


def test_custom_base_conversion1():
    obs = dt.units.conversionFactor("t oil_equivalent/capita", "MJ/capita")
    exp = 41868
    npt.assert_almost_equal(obs, exp)


def test_GWP_conversion_N2O():
    obs = dt.units.conversionFactor("Mt N2O", "Gg CO2eq", context="AR4GWP100")
    exp = 298000
    npt.assert_almost_equal(obs, exp)


def test_GWP_conversion_CH4():
    obs = dt.units.conversionFactor("Mt CH4", "Mt CO2eq", context="AR4GWP100")
    exp = 25
    npt.assert_almost_equal(obs, exp)


def test_GWP_AR6_conversion_CH4():
    obs = dt.units.conversionFactor("Mt CH4", "Mt CO2eq", context="AR5GWP100")
    exp = 28
    npt.assert_almost_equal(obs, exp)


def test_context_and_missing_space():
    obs = dt.units.conversionFactor("MtCH4", "MtCO2eq", context="AR5GWP100")
    exp = 28
    npt.assert_almost_equal(obs, exp)


def test_HFC_units():
    dt.core.unit_registry.ur("HFC134aeq")


def test_unique_conversion():
    assert dt.units.conversionFactor("%", "fraction") == 0.01
    assert dt.units.conversionFactor("fraction", "percent") == 100


def test_function_getUnit():
    dt.core.getUnit("°C")
    dt.core.getUnit("$")
    dt.core.getUnit("€")


def test_is_valid_unit():
    assert dt.core.is_validt_unit("m/s")

    assert not dt.core.is_validt_unit("no_unit")
