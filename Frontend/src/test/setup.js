import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeEach, vi } from "vitest";

beforeEach(() => {
  vi.stubGlobal("alert", vi.fn());
  vi.stubGlobal(
    "fetch",
    vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: async () => ({}),
      }),
    ),
  );

  if (!window.URL.createObjectURL) {
    window.URL.createObjectURL = vi.fn(() => "blob:mock-url");
  } else {
    vi.spyOn(window.URL, "createObjectURL").mockReturnValue("blob:mock-url");
  }

  if (!window.URL.revokeObjectURL) {
    window.URL.revokeObjectURL = vi.fn();
  } else {
    vi.spyOn(window.URL, "revokeObjectURL").mockImplementation(() => {});
  }

  vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});
