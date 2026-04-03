import { beforeEach, describe, expect, test } from "@jest/globals";
import request from "supertest";
import {
  app,
  generateGeminiInsightsMock,
  prismaMock,
  resetBackendMocks,
} from "./testHelpers.js";

describe("Historical API", () => {
  beforeEach(() => {
    // Clear all fake data before each test.
    resetBackendMocks();
  });

  test("rejects request when required fields are missing", async () => {
    // If required filters are missing, backend should stop early.
    const response = await request(app).post("/api/v1/historical").send({
      country: "PAK",
      start_year: 2020,
    });

    expect(response.status).toBe(400);
    expect(response.body.error).toMatch(/required/i);
  });

  test("returns not found when country does not exist", async () => {
    // Fake a failed country lookup.
    prismaMock.$queryRaw.mockResolvedValueOnce([]);

    const response = await request(app).post("/api/v1/historical").send({
      country: "XXX",
      sector_name: "transportation",
      start_year: 2020,
      end_year: 2024,
    });

    expect(response.status).toBe(404);
    expect(response.body.error).toBe("Country not found");
  });

  test("returns aggregated data for a valid request", async () => {
    // Mock each database step in the same order used by the controller.
    prismaMock.$queryRaw
      .mockResolvedValueOnce([{ id: 1 }])
      .mockResolvedValueOnce([{ id: 10 }])
      .mockResolvedValueOnce([
        { id: 100, name: "Road Transport" },
        { id: 101, name: "Aviation" },
      ])
      .mockResolvedValueOnce([{ id: 5 }])
      .mockResolvedValueOnce([
        { subsector_id: 100, year: 2020, total_emission: 100 },
        { subsector_id: 101, year: 2020, total_emission: 50 },
        { subsector_id: 100, year: 2021, total_emission: 120 },
      ])
      .mockResolvedValueOnce([
        { name: "co2", total: 220 },
        { name: "ch4", total: 20 },
        { name: "nox", total: 30 },
      ]);

    // Fake the text insight returned by Gemini.
    generateGeminiInsightsMock.mockResolvedValue(
      "Transport emissions remain dominated by road activity.",
    );

    // Send a valid request.
    const response = await request(app).post("/api/v1/historical").send({
      country: "PAK",
      sector_name: "transportation",
      gas_name: "co2",
      start_year: 2020,
      end_year: 2021,
    });

    expect(response.status).toBe(200);
    expect(response.body.total_emission_overall).toBe(270);
    expect(response.body.top_emitting_subsector).toBe("Road Transport");
    expect(response.body.llm_insights).toMatch(/road activity/i);
  });
});
