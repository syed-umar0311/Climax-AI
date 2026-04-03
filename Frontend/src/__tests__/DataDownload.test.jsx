import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

vi.mock("../utils/api", () => ({
  apiFetch: vi.fn(),
}));

import * as apiModule from "../utils/api";
import DataDownload from "../Pages/DataDownload.jsx";

function getYearSelects() {
  const selects = screen.getAllByRole("combobox");

  return {
    startYearSelect: selects[0],
    endYearSelect: selects[1],
  };
}

function createFakeDownloadAnchor() {
  const originalCreateElement = document.createElement.bind(document);
  let createdAnchor = null;

  vi.spyOn(document, "createElement").mockImplementation((tagName, options) => {
    const element = originalCreateElement(tagName, options);

    if (tagName === "a") {
      createdAnchor = element;
      element.click = vi.fn();
    }

    return element;
  });

  return () => createdAnchor;
}

describe("DataDownload", () => {
  beforeEach(() => {
    // Clear previous API calls.
    apiModule.apiFetch.mockReset();

    // Fake browser download helpers used by the component.
    vi.spyOn(URL, "createObjectURL").mockReturnValue("blob:download-url");
    vi.spyOn(URL, "revokeObjectURL").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("shows error when start year is greater than end year", () => {
    // Goal:
    // 1. Select invalid year range
    // 2. Click Get Data
    // 3. Check validation message
    render(<DataDownload />);
    const { startYearSelect, endYearSelect } = getYearSelects();

    fireEvent.change(startYearSelect, { target: { value: "2025" } });
    fireEvent.change(endYearSelect, { target: { value: "2020" } });
    fireEvent.click(screen.getByRole("button", { name: /get data/i }));

    expect(
      screen.getByText(/start year cannot be greater than end year/i),
    ).toBeInTheDocument();
    expect(apiModule.apiFetch).not.toHaveBeenCalled();
  });

  test("fetches preview data and downloads CSV", async () => {
    // Goal:
    // 1. Mock API response
    // 2. Load preview data
    // 3. Click Download CSV
    // 4. Check that browser download started
    const getCreatedAnchor = createFakeDownloadAnchor();

    apiModule.apiFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        status: "success",
        rowCount: 1,
        filters: {
          region: null,
          gas: null,
          startYear: 2024,
          endYear: 2024,
        },
        columns: [
          "year",
          "region",
          "gas",
          "sector",
          "subsector",
          "emission_value",
        ],
        rows: [
          {
            year: 2024,
            region: "Pakistan",
            gas: "co2",
            sector: "Transportation",
            subsector: "Road Transport",
            emission_value: 123.45,
          },
        ],
      }),
    });

    render(<DataDownload />);
    const { startYearSelect, endYearSelect } = getYearSelects();

    fireEvent.change(startYearSelect, { target: { value: "2024" } });
    fireEvent.change(endYearSelect, { target: { value: "2024" } });
    fireEvent.click(screen.getByRole("button", { name: /get data/i }));

    await waitFor(() => {
      expect(apiModule.apiFetch).toHaveBeenCalled();
      expect(screen.getByText(/data preview/i)).toBeInTheDocument();
      expect(screen.getByText("Pakistan")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: /download csv/i }));
    const createdAnchor = getCreatedAnchor();

    expect(URL.createObjectURL).toHaveBeenCalledTimes(1);
    expect(createdAnchor.download).toMatch(/\.csv$/);
    expect(createdAnchor.click).toHaveBeenCalledTimes(1);
  });
});
