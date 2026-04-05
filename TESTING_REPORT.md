# FYP Testing Report

## Overview
This testing framework was designed for a full-stack Final Year Project that combines an Express backend, a React frontend, a Python-based prediction model, and Selenium-driven end-to-end user journeys. The framework follows both white-box and black-box principles to ensure that internal logic, external behavior, and user-facing workflows are validated in a structured and academically defensible manner.

## Testing Strategy
The framework implements the following complementary testing layers:

| Testing Type | Purpose | Current Implementation |
| --- | --- | --- |
| Unit Testing | Verifies isolated logic units and internal decision paths | Backend controller-route behavior with mocked dependencies, frontend component logic, model preprocessing and inference functions |
| Integration Testing | Confirms correct interaction between modules | Express route tests with mocked database/model boundaries, frontend page tests with mocked API utilities |
| System Testing | Evaluates complete feature behavior from the user perspective | Selenium scenarios covering login, prediction, visualization, and CSV download workflows |
| Regression Testing | Prevents previously working behavior from silently breaking | Re-runnable automated suites executed through a single orchestration command |
| Validation Testing | Confirms the system satisfies functional FYP requirements | Auth, historical analytics, predictions, downloads, explainability-oriented output handling, and report generation are all mapped to project features |

## White-Box and Black-Box Coverage
White-box testing is represented through unit and integration tests that target the internal control flow of controllers, page logic, utility methods, and model preprocessing/inference behavior. These tests intentionally inspect validation branches, route decisions, transformed payloads, and aggregation logic.

Black-box testing is represented through Selenium automation that interacts with the application harness in the same manner as an end user. These tests do not depend on implementation details and instead validate externally visible behavior such as login success feedback, prediction execution, visualization display, and CSV download signaling.

## Tools and Frameworks
- Backend: Jest with Supertest
- Frontend: React Testing Library with the existing Vitest runner in this Vite-based frontend
- Model: PyTest
- End-to-End: Selenium for browser-driven black-box testing
- Reporting: JSON, JUnit XML, pytest-html, and a custom Node.js merge script producing `/reports/final-report.html`

## Test Design Approach
Backend tests were written around the current Express route structure and mock the MongoDB, Prisma, and Gemini integration boundaries. This allows route behavior, validation, error handling, and response contracts to be verified without requiring live infrastructure.

Frontend tests focus on component behavior, page-level API integration, loading and error states, and user-triggered actions such as downloads. Child components with heavy charting behavior are mocked where appropriate so that the tests remain stable and focused on feature correctness.

Model tests validate the preprocessing pipeline, default coordinate handling, subsector sequence generation, and prediction aggregation. This ensures that the AI pipeline remains inspectable rather than treated as a purely opaque artifact.

Selenium tests automate representative user journeys that are directly relevant to the FYP context: authentication, prediction execution, visualization rendering, and CSV download behavior.

## Intentional Failing Tests
Not all tests are expected to pass. Approximately 10-20% of the suite has been intentionally designed to fail in a meaningful way. This is an intentional academic decision for the FYP demonstration because it shows that the framework can detect:

- Incorrect expected API semantics
- UI label mismatches
- Invalid model output expectations
- Visualization assertion mismatches

These failures are not random. They demonstrate the robustness of the framework by proving that it can surface genuine deviations between expected and actual behavior.

## Coverage of FYP Requirements
The framework maps directly to the core functional areas of the project:

- Authentication testing validates signup, login, token refresh, logout, and history persistence behavior.
- Prediction testing validates forecasting requests, payload handling, and prediction result rendering.
- Historical and explainability-oriented analytics testing validates sector and gas-based response structures, ratio calculations, and insight attachment behavior.
- Data export testing validates input filtering, response shaping, preview rendering, and CSV generation behavior.
- Usability and validation testing are represented through form validation, loading states, error visibility, and realistic Selenium user flows.

## Execution
The entire framework is orchestrated through one command:

```bash
npm run test:all
```

This command executes backend, frontend, model, and Selenium suites, captures raw outputs, and generates the combined HTML report at:

```text
reports/final-report.html
```

## Academic Conclusion
This testing framework provides a balanced and FYP-appropriate quality assurance strategy. It demonstrates internal logic verification, user-facing validation, regression readiness, and evidence-based reporting. The inclusion of meaningful failing tests strengthens the academic value of the framework by showing that the suite is capable of detecting defects, not merely confirming success cases.
