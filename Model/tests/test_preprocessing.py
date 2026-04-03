import numpy as np

from api_utils.preprocessing import preprocess_input


def create_scaler(means, stds):
    # The real code expects a dictionary with means and standard deviations.
    return {
        "means": np.array(means, dtype=np.float64),
        "stds": np.array(stds, dtype=np.float64),
    }


def create_indexers(country, sector, subsector, gas):
    # These dictionaries act like the lookup tables used by the model code.
    return {
        "iso3_country": country,
        "sector": sector,
        "subsector": subsector,
        "gas": gas,
    }


def test_preprocess_input_uses_default_coordinates_when_lat_lon_are_missing(monkeypatch):
    # Goal:
    # 1. User sends no lat/lon
    # 2. Function should use default coordinates
    monkeypatch.setattr("api_utils.preprocessing.get_default_lat_lon", lambda country: (30.0, 70.0))
    monkeypatch.setattr("api_utils.preprocessing.get_subsectors", lambda sector: ["road-transport"])
    monkeypatch.setattr("api_utils.preprocessing.get_month_duration", lambda year, month: 30)

    scaler_model = create_scaler([0.0, 0.0, 30.0, 2020.0], [10.0, 10.0, 5.0, 10.0])
    indexers = create_indexers(
        {"PAK": 1},
        {"transportation": 2},
        {"road-transport": 3},
        {"co2": 4},
    )

    result = preprocess_input(
        {
            "country": "PAK",
            "sector": "transportation",
            "gas": "co2",
            "year": 2025,
            "lat": None,
            "lon": None,
        },
        scaler_model,
        indexers,
    )

    # One subsector should be produced.
    assert set(result.keys()) == {"road-transport"}
    sequence = result["road-transport"]

    # Sequence shape = 12 months x 10 features.
    assert sequence.shape == (12, 10)

    # First 4 values are encoded categorical features.
    np.testing.assert_allclose(sequence[0][:4], np.array([1, 2, 3, 4]))

    # Next values are scaled numeric features.
    np.testing.assert_allclose(sequence[0][4:8], np.array([3.0, 7.0, 0.0, 0.5]))


def test_preprocess_input_preserves_explicit_coordinates(monkeypatch):
    # Goal:
    # 1. User sends lat/lon
    # 2. Function should keep them instead of default coordinates
    monkeypatch.setattr("api_utils.preprocessing.get_default_lat_lon", lambda country: (99.0, 99.0))
    monkeypatch.setattr("api_utils.preprocessing.get_subsectors", lambda sector: ["aviation"])
    monkeypatch.setattr("api_utils.preprocessing.get_month_duration", lambda year, month: 31)

    scaler_model = create_scaler([10.0, 20.0, 30.0, 2020.0], [10.0, 10.0, 1.0, 10.0])
    indexers = create_indexers(
        {"PAK": 1},
        {"transportation": 2},
        {"aviation": 5},
        {"ch4": 6},
    )

    result = preprocess_input(
        {
            "country": "PAK",
            "sector": "transportation",
            "gas": "ch4",
            "year": 2025,
            "lat": 40.0,
            "lon": 50.0,
        },
        scaler_model,
        indexers,
    )

    sequence = result["aviation"]
    np.testing.assert_allclose(sequence[0][4:8], np.array([3.0, 3.0, 1.0, 0.5]))
