import { jest } from "@jest/globals";

// These are the shared fake modules used by all backend tests.
// We mock them once here so each test file can stay small and focused.
export const userModelMock = {
  findOne: jest.fn(),
  create: jest.fn(),
  findById: jest.fn(),
  findOneAndUpdate: jest.fn(),
};

export const prismaMock = {
  $queryRaw: jest.fn(),
  $queryRawUnsafe: jest.fn(),
};

export const jwtMock = {
  verify: jest.fn(),
};

export const generateGeminiInsightsMock = jest.fn();

await jest.unstable_mockModule("../src/models/user.model.js", () => ({
  default: userModelMock,
}));

await jest.unstable_mockModule("../src/db/prisma.js", () => ({
  default: prismaMock,
}));

await jest.unstable_mockModule("../src/utils/gemini.js", () => ({
  generateGeminiInsights: generateGeminiInsightsMock,
}));

await jest.unstable_mockModule("jsonwebtoken", () => ({
  default: jwtMock,
}));

// Import the Express app only after the mocks are ready.
export const { default: app } = await import("../src/app.js");

export function resetBackendMocks() {
  jest.clearAllMocks();
}

export function setAuthEnv() {
  process.env.CORS_ORIGIN = "http://localhost:5173";
  process.env.ACCESS_TOKEN_SECRET = "access-secret";
  process.env.ACCESS_TOKEN_EXPIRY = "15m";
  process.env.REFRESH_TOKEN_SECRET = "refresh-secret";
  process.env.REFRESH_TOKEN_EXPIRY = "7d";
}
