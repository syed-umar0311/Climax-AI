import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";

import ForecastsConfiguration from "../components/ForecastsConfiguration.jsx";

function getForecastFormSelects() {
  const selects = screen.getAllByRole("combobox");

  return {
    regionSelect: selects[0],
    sectorSelect: selects[1],
    gasSelect: selects[2],
    yearSelect: selects[3],
  };
}

describe("ForecastsConfiguration", () => {
  test("sends the selected values in the forecast request", () => {
    // Goal:
    // 1. Change the dropdown values
    // 2. Submit the form
    // 3. Check the payload sent to fetchPrediction
    const fetchPrediction = vi.fn();

    render(<ForecastsConfiguration fetchPrediction={fetchPrediction} />);
    const form = getForecastFormSelects();

    fireEvent.change(form.regionSelect, { target: { value: "IND" } });
    fireEvent.change(form.sectorSelect, { target: { value: "power" } });
    fireEvent.change(form.gasSelect, { target: { value: "n2o" } });
    fireEvent.change(form.yearSelect, { target: { value: "2030" } });
    fireEvent.click(screen.getByRole("button", { name: /generate forecasts/i }));

    expect(fetchPrediction).toHaveBeenCalledWith({
      country: "IND",
      sector: "power",
      gas: "n2o",
      year: "2030",
      month: 1,
    });
  });
});
