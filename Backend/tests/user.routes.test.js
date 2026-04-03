import { beforeEach, describe, expect, jest, test } from "@jest/globals";
import request from "supertest";
import {
  app,
  resetBackendMocks,
  setAuthEnv,
  userModelMock,
} from "./testHelpers.js";

describe("User API", () => {
  beforeEach(() => {
    // Reset mocks so one test does not affect the next test.
    resetBackendMocks();
    setAuthEnv();
  });

  test("rejects signup when required fields are missing", async () => {
    // Step 1: send incomplete signup data.
    // Step 2: backend should reject it.
    const response = await request(app)
      .post("/api/v1/user/signup")
      .send({ email: "qa@test.com", password: "secret12" });

    expect(response.status).toBe(400);
    expect(response.body.message).toMatch(/missing required fields/i);
  });

  test("logs in successfully with correct credentials", async () => {
    // Create a fake user object that behaves like a real MongoDB user document.
    const savedUser = {
      _id: "user-1",
      email: "qa@test.com",
      fullName: "QA Engineer",
      comparePassword: jest.fn().mockResolvedValue(true),
      generateAccessToken: jest.fn().mockReturnValue("access-token"),
      generateRefreshToken: jest.fn().mockReturnValue("refresh-token"),
      save: jest.fn().mockResolvedValue(undefined),
    };

    // When backend asks for the user, return our fake user.
    userModelMock.findOne.mockResolvedValue(savedUser);

    // When backend asks for the public user data, return this clean object.
    userModelMock.findById.mockReturnValue({
      select: jest.fn().mockResolvedValue({
        _id: "user-1",
        email: "qa@test.com",
        fullName: "QA Engineer",
      }),
    });

    // Send login request.
    const response = await request(app).post("/api/v1/user/login").send({
      email: "qa@test.com",
      password: "secret12",
    });

    expect(response.status).toBe(200);
    expect(response.body.status).toBe("success");
    expect(response.body.accessToken).toBe("access-token");
    expect(response.body.refreshToken).toBe("refresh-token");
  });

  test("rejects refresh token request when token is missing", async () => {
    // If refresh token is not provided, backend should return 401.
    const response = await request(app).post("/api/v1/user/refresh-token").send({});

    expect(response.status).toBe(401);
    expect(response.body.message).toBe("Refresh token is missing");
  });
});
