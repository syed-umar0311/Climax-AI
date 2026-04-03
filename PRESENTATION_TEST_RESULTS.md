# Test Results For Presentation

## Why All Automated Tests Pass

This is normal.

Automated tests are written to check whether the current unit logic works correctly.
If the code behaves as expected in those specific scenarios, the tests should pass.

To show **both passed and failed cases** in front of the teacher:

- show **automated test pass cases**
- show **manual/system failed cases** based on real problems found in the project

This is the honest and professional way to present testing results.

## 1. Passed Cases

### Frontend Passed Cases

| Test ID | What It Checks | Result |
|---|---|---|
| FE-PASS-001 | Login form sends correct request and calls success callback | Passed |
| FE-PASS-002 | Signup form blocks submission when passwords do not match | Passed |
| FE-PASS-003 | Forecast form sends selected country, sector, gas, and year correctly | Passed |
| FE-PASS-004 | Download page blocks invalid year range | Passed |
| FE-PASS-005 | Download page shows preview data and starts CSV download | Passed |
| FE-PASS-006 | Prediction page loads prediction data and saves user history | Passed |

### Backend Passed Cases

| Test ID | What It Checks | Result |
|---|---|---|
| BE-PASS-001 | Signup fails when required fields are missing | Passed |
| BE-PASS-002 | Login succeeds with valid credentials | Passed |
| BE-PASS-003 | Refresh token endpoint rejects missing token | Passed |
| BE-PASS-004 | Data download rejects missing years | Passed |
| BE-PASS-005 | Data download rejects invalid year range | Passed |
| BE-PASS-006 | Data download returns normalized rows for valid request | Passed |
| BE-PASS-007 | Historical API rejects missing filters | Passed |
| BE-PASS-008 | Historical API returns 404 for unknown country | Passed |
| BE-PASS-009 | Historical API returns aggregated emissions for valid request | Passed |

### Model Passed Cases

| Test ID | What It Checks | Result |
|---|---|---|
| ML-PASS-001 | Preprocessing uses default coordinates when lat/lon are missing | Passed |
| ML-PASS-002 | Preprocessing keeps user coordinates when lat/lon are provided | Passed |
| ML-PASS-003 | Inference adds totals correctly when multiple subsectors exist | Passed |
| ML-PASS-004 | Inference handles single subsector correctly | Passed |

## 2. Failed Cases

These are **real failed cases** found during project review.

### FAIL-001: Explainability API Is Not Available

| Field | Detail |
|---|---|
| Module | Model API |
| Scenario | Call `/api/explain` to get SHAP/XAI result |
| Expected Result | API should return explainability output |
| Actual Result | Endpoint is not available because the route is commented out |
| Status | Failed |
| Evidence | [app.py](/d:/FYP/Model/app.py) |

How to explain:
The project contains explainability logic files, but the API route is currently disabled, so end-to-end explainability testing fails.

### FAIL-002: Signup Password Rule Is Inconsistent

| Field | Detail |
|---|---|
| Module | Frontend + Backend |
| Scenario | User enters a 6-character password during signup |
| Expected Result | System should follow one clear rule everywhere |
| Actual Result | Frontend text says minimum 8 characters, but backend accepts 6 characters |
| Status | Failed |
| Evidence | [AuthModal.jsx](/d:/FYP/Frontend/src/Pages/AuthModal.jsx), [user.controlers.js](/d:/FYP/Backend/src/controllers/user.controlers.js), [user.model.js](/d:/FYP/Backend/src/models/user.model.js) |

How to explain:
This is a validation mismatch. The UI message and backend logic do not fully agree.

### FAIL-003: Prediction Page Can Stay Stuck In Loading State On API Error

| Field | Detail |
|---|---|
| Module | Frontend Prediction Page |
| Scenario | Prediction API fails or is turned off |
| Expected Result | Loading should stop and an error message should appear |
| Actual Result | `loading` is never reset to `false` inside the `catch` block |
| Status | Failed |
| Evidence | [Prediction.jsx](/d:/FYP/Frontend/src/Pages/Prediction.jsx) |

How to reproduce:
1. Stop the Flask model API.
2. Open Prediction page.
3. The loader may remain visible because the error path does not call `setLoading(false)`.

### FAIL-004: Dashboard Page Can Stay Stuck In Loading State On API Error

| Field | Detail |
|---|---|
| Module | Frontend Dashboard Page |
| Scenario | Historical API fails or backend is turned off |
| Expected Result | Loading should stop and user should see an error state |
| Actual Result | `loading` is never reset to `false` inside the `catch` block |
| Status | Failed |
| Evidence | [Dashboard.jsx](/d:/FYP/Frontend/src/Pages/Dashboard.jsx) |

How to reproduce:
1. Stop the backend server.
2. Open Dashboard page.
3. Skeleton/loading screen can remain because the error path does not clear loading state.

## 3. Best Way To Show This In Viva

Show this in 2 parts:

### Part A: Passed Automated Cases

Run:

```powershell
cd d:\FYP\Frontend
npx vitest run

cd d:\FYP\Backend
npm test

cd d:\FYP\Model
.\.venv310\Scripts\python.exe -m pytest tests -q
```

Then say:

- Frontend unit/integration-style tests passed
- Backend API tests passed
- Model preprocessing and inference tests passed

### Part B: Failed Real Cases

Then explain these real failures:

1. Explainability endpoint is not active
2. Signup password rule is inconsistent
3. Prediction page loading is not cleared on API error
4. Dashboard loading is not cleared on API error

## 4. One-Line Presentation Summary

You can say this:

“Automated unit tests for frontend, backend, and model passed successfully, but system-level review still identified real failed cases, including disabled explainability API, inconsistent password validation, and loading-state handling issues in frontend error scenarios.”
