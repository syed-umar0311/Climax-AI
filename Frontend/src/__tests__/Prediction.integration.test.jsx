import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";

vi.mock("../utils/api", () => ({
  apiFetch: vi.fn(),
  predictionFetch: vi.fn(),
}));

vi.mock("../components/EmissionPrediction.jsx", () => ({
  default: ({ prediction }) => (
    <div>Emission Prediction Total: {prediction.data.total_emissions}</div>
  ),
}));

vi.mock("../components/MonthlyTrends.jsx", () => ({
  default: () => <div>Monthly Trends Ready</div>,
}));

vi.mock("../components/LLMResponse.jsx", () => ({
  default: ({ response }) => <div>Insight: {response}</div>,
}));

import * as apiModule from "../utils/api";
import Prediction from "../Pages/Prediction.jsx";

function createPredictionApiResponse() {
  return {
    ok: true,
    json: async () => ({
      meta: {
        country: "PAK",
        sector: "transportation",
        year: 2025,
        requested_gas: "co2",
      },
      data: {
        total_emissions: 321.5,
        monthly_trends: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        gas_composition: {
          ratios: { co2: 80, ch4: 15, n2o: 5 },
          absolute_totals: { co2: 250, ch4: 50, n2o: 21.5 },
          total_combined: 321.5,
        },
        subsector_breakdown: [],
      },
      llm_insights: "Transport emissions stay elevated in the forecast horizon.",
    }),
  };
}

describe("Prediction page", () => {
  beforeEach(() => {
    // Reset both API mocks before each test.
    apiModule.apiFetch.mockReset();
    apiModule.predictionFetch.mockReset();
  });

  test("loads prediction data on page start and stores user history", async () => {
    // Goal:
    // 1. Page loads
    // 2. Prediction API is called
    // 3. History API is called
    // 4. Result components appear on screen
    apiModule.predictionFetch.mockResolvedValue(createPredictionApiResponse());

    apiModule.apiFetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: "success" }),
    });

    render(<Prediction userEmail="qa@test.com" />);

    await waitFor(() => {
      expect(apiModule.predictionFetch).toHaveBeenCalledWith(
        "/api/predict",
        expect.objectContaining({ method: "POST" }),
      );
      expect(apiModule.apiFetch).toHaveBeenCalledWith(
        "/api/v1/user/history",
        expect.objectContaining({ method: "POST" }),
      );
      expect(screen.getByText(/Emission Prediction Total: 321.5/i)).toBeInTheDocument();
      expect(screen.getByText(/Monthly Trends Ready/i)).toBeInTheDocument();
      expect(screen.getByText(/Insight: Transport emissions stay elevated/i)).toBeInTheDocument();
    });
  });
});
