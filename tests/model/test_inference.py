import numpy as np

from api_utils.inference import run_inference


class StubModel:
    def predict(self, _inputs):
        return np.array([np.log1p(np.arange(1, 13, dtype=float))])


def build_preprocessed_data():
    sequence = np.ones((12, 10), dtype=float)
    return {
      "road-transportation": sequence,
      "domestic-aviation": sequence,
    }


def test_run_inference_aggregates_subsector_predictions():
    from api_utils import inference

    inference.preprocess_input = lambda *_args, **_kwargs: build_preprocessed_data()

    result = run_inference(
        {"country": "PAK"},
        StubModel(),
        scaler_model={},
        indexers={},
    )

    assert isinstance(result["monthly_emissions"], list)
    assert len(result["monthly_emissions"]) == 12


def test_run_inference_with_mocked_preprocessing(monkeypatch):
    monkeypatch.setattr(
        "api_utils.inference.preprocess_input",
        lambda *_args, **_kwargs: build_preprocessed_data(),
    )

    result = run_inference(
        {"country": "PAK"},
        StubModel(),
        scaler_model={},
        indexers={},
    )

    assert set(result["subsector_emissions"].keys()) == {
        "road-transportation",
        "domestic-aviation",
    }
    assert result["monthly_emissions"][0] == 2.0
    assert result["monthly_emissions"][-1] == 24.0
    assert result["total_emissions"] == sum(range(1, 13)) * 2


def test_intentional_failure_model_outputs_should_not_all_be_zero(monkeypatch):
    monkeypatch.setattr(
        "api_utils.inference.preprocess_input",
        lambda *_args, **_kwargs: build_preprocessed_data(),
    )

    result = run_inference(
        {"country": "PAK"},
        StubModel(),
        scaler_model={},
        indexers={},
    )

    assert result["total_emissions"] == 0
