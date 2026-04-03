import numpy as np

from api_utils.inference import run_inference


class DummyModel:
    def predict(self, inputs):
        # Return the same prediction for all 12 months.
        # np.log1p is used because the real code later applies np.expm1.
        return np.log1p(np.array([[1.0] * 12], dtype=np.float64))


def fake_preprocessed_data(*subsector_names):
    # Build simple 12 x 10 fake sequences for each subsector.
    fake_sequence = np.zeros((12, 10), dtype=np.float64)
    return {name: fake_sequence for name in subsector_names}


def test_run_inference_aggregates_multiple_subsector_paths(monkeypatch):
    # Goal:
    # 1. Pretend preprocessing returned 2 subsectors
    # 2. Check that inference adds both together

    monkeypatch.setattr(
        "api_utils.inference.preprocess_input",
        lambda user_input, scaler_model, indexers: fake_preprocessed_data(
            "road-transport",
            "aviation",
        ),
    )

    result = run_inference(
        {"country": "PAK", "sector": "transportation", "gas": "co2", "year": 2025},
        DummyModel(),
        scaler_model={},
        indexers={},
    )

    # Each subsector gives 1.0 for every month.
    # With 2 subsectors, each month becomes 2.0.
    assert set(result["subsector_emissions"].keys()) == {"road-transport", "aviation"}
    assert result["monthly_emissions"] == [2.0] * 12
    assert result["total_emissions"] == 24.0
    assert result["subsector_emissions"]["road-transport"]["total_emissions"] == 12.0


def test_run_inference_handles_single_subsector_without_overcounting(monkeypatch):
    # Goal:
    # 1. Pretend preprocessing returned only 1 subsector
    # 2. Check that totals stay correct

    monkeypatch.setattr(
        "api_utils.inference.preprocess_input",
        lambda user_input, scaler_model, indexers: fake_preprocessed_data("buildings"),
    )

    result = run_inference(
        {"country": "PAK", "sector": "buildings", "gas": "nox", "year": 2025},
        DummyModel(),
        scaler_model={},
        indexers={},
    )

    assert result["monthly_emissions"] == [1.0] * 12
    assert result["total_emissions"] == 12.0
    assert result["subsector_emissions"]["buildings"]["monthly_emissions"] == [1.0] * 12
