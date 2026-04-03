import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, test, vi } from "vitest";

vi.mock("../utils/api", () => ({
  apiFetch: vi.fn(),
}));

import * as apiModule from "../utils/api";
import AuthModal from "../Pages/AuthModal.jsx";

function getLoginInputs(container) {
  return {
    emailInput: container.querySelector('input[type="email"]'),
    passwordInput: container.querySelector('input[type="password"]'),
  };
}

function fillSignupForm(container) {
  const inputs = container.querySelectorAll("input");

  return {
    fullNameInput: inputs[0],
    emailInput: inputs[1],
    passwordInput: inputs[2],
    confirmPasswordInput: inputs[3],
  };
}

describe("AuthModal", () => {
  beforeEach(() => {
    // Remove old API calls from previous tests.
    apiModule.apiFetch.mockReset();

    // Fake the browser alert box so tests can check its message.
    vi.stubGlobal("alert", vi.fn());
  });

  test("logs in successfully with valid email and password", async () => {
    // Goal:
    // 1. Fill the login form
    // 2. Click Sign In
    // 3. Check that API and success callback were called
    const onLoginSuccess = vi.fn();

    apiModule.apiFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        status: "success",
        message: "Login successful",
        user: { email: "qa@test.com", fullName: "QA Engineer" },
      }),
    });

    const { container } = render(<AuthModal onLoginSuccess={onLoginSuccess} />);
    const { emailInput, passwordInput } = getLoginInputs(container);

    fireEvent.change(emailInput, { target: { value: "qa@test.com" } });
    fireEvent.change(passwordInput, { target: { value: "secret12" } });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(apiModule.apiFetch).toHaveBeenCalledWith(
        "/api/v1/user/login",
        expect.any(Object),
      );
      expect(onLoginSuccess).toHaveBeenCalledWith({
        email: "qa@test.com",
        fullName: "QA Engineer",
      });
    });
  });

  test("shows alert when signup passwords do not match", () => {
    // Goal:
    // 1. Open signup form
    // 2. Enter two different passwords
    // 3. Check that alert is shown and API is not called
    const { container } = render(<AuthModal onLoginSuccess={vi.fn()} />);

    fireEvent.click(screen.getByRole("button", { name: /create one/i }));
    const signupForm = fillSignupForm(container);

    fireEvent.change(signupForm.fullNameInput, { target: { value: "QA Engineer" } });
    fireEvent.change(signupForm.emailInput, { target: { value: "qa@test.com" } });
    fireEvent.change(signupForm.passwordInput, { target: { value: "secret12" } });
    fireEvent.change(signupForm.confirmPasswordInput, {
      target: { value: "different123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /create account/i }));

    expect(alert).toHaveBeenCalledWith("Passwords do not match");
    expect(apiModule.apiFetch).not.toHaveBeenCalled();
  });
});
