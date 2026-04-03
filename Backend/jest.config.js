export default {
  testEnvironment: "node",
  roots: ["<rootDir>/tests"],
  testMatch: ["**/*.test.js"],
  collectCoverageFrom: [
    "src/**/*.js",
    "!src/index.js",
    "!src/db/**/*.js",
    "!src/constants.js",
  ],
  coverageDirectory: "coverage",
  transform: {},
};
