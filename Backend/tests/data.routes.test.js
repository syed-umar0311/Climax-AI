import { beforeEach, describe, expect, test } from "@jest/globals";
import request from "supertest";
import { app, prismaMock, resetBackendMocks } from "./testHelpers.js";

describe("Data Download API", () => {
  beforeEach(() => {
    // Start each test with clean mocks.
    resetBackendMocks();
  });

  test("rejects request when years are missing", async () => {
    // Missing startYear/endYear should fail before database code runs.
    const response = await request(app).get("/api/v1/data/download?region=pak");

    expect(response.status).toBe(400);
    expect(response.body.message).toBe("startYear and endYear are required");
  });

  test("rejects request when start year is greater than end year", async () => {
    // Invalid year range should also return a validation error.
    const response = await request(app).get(
      "/api/v1/data/download?startYear=2025&endYear=2020",
    );

    expect(response.status).toBe(400);
    expect(response.body.message).toBe(
      "startYear must be less than or equal to endYear",
    );
  });

  test("returns normalized rows for a valid request", async () => {
    // Fake one database row.
    prismaMock.$queryRawUnsafe.mockResolvedValue([
      {
        emission: "123.45",
        year: 2024,
        region_name: "Pakistan",
        gas_name: "nox",
        subsector_name: "Road Transport",
        sector_name: "Transportation",
      },
    ]);

    // Send a valid request and check the formatted response.
    const response = await request(app).get(
      "/api/v1/data/download?region=pakistan&gas=n2o&startYear=2024&endYear=2024",
    );

    expect(response.status).toBe(200);
    expect(response.body.status).toBe("success");
    expect(response.body.rowCount).toBe(1);
    expect(response.body.rows[0].emission_value).toBe(123.45);
  });
});
