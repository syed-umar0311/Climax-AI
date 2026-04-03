# GHG Emissions Forecasting System - QA Testing Suite

## 1. Introduction

This document presents a complete and professional testing suite for the Final Year Project titled **Web-Based GHG Emissions Forecasting System**. The system under test consists of:

- A React-based frontend for authentication, forecasting, historical visualization, and data download
- A Node.js/Express backend for authentication, user history, historical analytics, and dataset export
- MongoDB for user accounts and user history
- PostgreSQL for emissions datasets and analytical queries
- A Flask/TensorFlow model API for emissions prediction

The suite covers black-box testing, white-box testing, integration testing, regression testing, usability testing, validation testing, and performance testing. It is structured for direct use in a university project report.

## 2. Scope and Assumptions

- Frontend authentication is implemented in [`Frontend/src/Pages/AuthModal.jsx`](/d:/FYP/Frontend/src/Pages/AuthModal.jsx).
- Forecast requests are sent directly from the frontend to the model API through [`Frontend/src/Pages/Prediction.jsx`](/d:/FYP/Frontend/src/Pages/Prediction.jsx).
- Historical charts and CSV download use Express backend APIs through [`Frontend/src/Pages/Dashboard.jsx`](/d:/FYP/Frontend/src/Pages/Dashboard.jsx) and [`Frontend/src/Pages/DataDownload.jsx`](/d:/FYP/Frontend/src/Pages/DataDownload.jsx).
- User accounts and history are handled by [`Backend/src/controllers/user.controlers.js`](/d:/FYP/Backend/src/controllers/user.controlers.js).
- Historical analytics and data export are handled by [`Backend/src/controllers/historical.controller.js`](/d:/FYP/Backend/src/controllers/historical.controller.js) and [`Backend/src/controllers/data.controller.js`](/d:/FYP/Backend/src/controllers/data.controller.js).
- Prediction is handled by [`Model/app.py`](/d:/FYP/Model/app.py) and [`Model/api_utils/inference.py`](/d:/FYP/Model/api_utils/inference.py).
- The repository contains explainability utilities in [`Model/api_utils/explainable_inference.py`](/d:/FYP/Model/api_utils/explainable_inference.py), but the Flask `/api/explain` route is currently commented out in [`Model/app.py`](/d:/FYP/Model/app.py). Therefore, explainability tests below are included as validation-ready tests for the project report and future activation.

## 3. Black-Box Testing

**Execution note:** the `Actual Output` and `Status` columns are intentionally left in a report-ready state because the full distributed system was not executed end-to-end in this environment.

### 3.1 User Authentication and Session Handling

| Test Case ID | Description | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| BB-AUTH-001 | Verify successful user signup with valid data | `fullName=Ali Khan`, `email=ali@test.com`, `password=secret12` | Account is created, HTTP `201`, success message returned, user object excludes password | Pending execution | Not Executed |
| BB-AUTH-002 | Verify signup validation when required fields are missing | Missing `fullName` or `email` or `password` | HTTP `400`, validation error message indicating missing required fields | Pending execution | Not Executed |
| BB-AUTH-003 | Verify signup rejects invalid email format | `email=alitest.com` | HTTP `400`, message `Invalid email format` | Pending execution | Not Executed |
| BB-AUTH-004 | Verify signup rejects weak password | `password=12345` | HTTP `400`, password length validation message | Pending execution | Not Executed |
| BB-AUTH-005 | Verify signup rejects duplicate email | Existing registered email | HTTP `409`, message `Email already registered` | Pending execution | Not Executed |
| BB-AUTH-006 | Verify login succeeds with valid credentials | Valid `email` and `password` | HTTP `200`, success response, access token and refresh token returned and stored as cookies | Pending execution | Not Executed |
| BB-AUTH-007 | Verify login fails with wrong password | Valid email, invalid password | HTTP `401`, message `Invalid email or password` | Pending execution | Not Executed |
| BB-AUTH-008 | Verify login fails when email/password is missing | Missing `email` or `password` | HTTP `400`, required-field validation message | Pending execution | Not Executed |
| BB-AUTH-009 | Verify refresh token endpoint renews session | Valid refresh token in cookie or request body | HTTP `200`, new access token and refresh token issued, user remains authenticated | Pending execution | Not Executed |
| BB-AUTH-010 | Verify refresh endpoint handles missing token | No refresh token provided | HTTP `401`, message `Refresh token is missing` | Pending execution | Not Executed |
| BB-AUTH-011 | Verify refresh endpoint rejects invalid or expired token | Tampered or expired refresh token | HTTP `401`, message indicating invalid or expired refresh token | Pending execution | Not Executed |
| BB-AUTH-012 | Verify logout clears session cookies | Valid logout request | HTTP `200`, success message, access and refresh cookies cleared | Pending execution | Not Executed |
| BB-AUTH-013 | Verify history entry storage after successful dashboard/prediction action | Authenticated user email with valid sector, gas, and year range | HTTP `201`, history record appended to user profile | Pending execution | Not Executed |
| BB-AUTH-014 | Verify history retrieval for valid user | Existing user email | HTTP `200`, array of past interactions returned | Pending execution | Not Executed |

### 3.2 Prediction API

| Test Case ID | Description | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| BB-PRED-001 | Verify successful forecast generation with valid minimum payload | `country=PAK`, `sector=transportation`, `gas=co2` | HTTP `200`, prediction response contains `meta`, `total_emissions`, `monthly_trends`, `subsector_breakdown`, and `gas_composition` | Pending execution | Not Executed |
| BB-PRED-002 | Verify forecast generation with explicit year and month boundary values | `year=2025`, `month=1` and `month=12` | HTTP `200`, forecast generated without validation failure | Pending execution | Not Executed |
| BB-PRED-003 | Verify API rejects invalid gas type | `gas=so2` | HTTP `400`, message `Invalid gas type` | Pending execution | Not Executed |
| BB-PRED-004 | Verify API rejects missing required fields | Missing `country` or `sector` or `gas` | HTTP `400`, message `Missing required fields` | Pending execution | Not Executed |
| BB-PRED-005 | Verify API error handling for unsupported sector/country combination | Unsupported `sector` or unknown `country` | Request is rejected gracefully with structured error payload | Pending execution | Not Executed |
| BB-PRED-006 | Verify API handles invalid numeric year value | `year=abcd` | Request is rejected gracefully and does not crash the service | Pending execution | Not Executed |
| BB-PRED-007 | Verify API maps `n2o` request to internal model gas label correctly | `gas=n2o` | HTTP `200`, request succeeds and output metadata still reports `requested_gas=n2o` | Pending execution | Not Executed |
| BB-PRED-008 | Verify API returns gas composition ratios and totals | Valid prediction request | `gas_composition.ratios`, `absolute_totals`, and `total_combined` are present and numerically consistent | Pending execution | Not Executed |
| BB-PRED-009 | Verify frontend handles model API outage | Prediction API unavailable | User receives visible error state, no stale charts are shown, application does not crash | Pending execution | Not Executed |

### 3.3 Explainability Output

| Test Case ID | Description | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| BB-XAI-001 | Verify explainability endpoint returns feature attribution output for a valid request | Valid explain request with `country`, `sector`, `gas`, `year`, `month` | HTTP `200`, attribution values returned for numerical and categorical features | Pending execution | Pending Endpoint Activation |
| BB-XAI-002 | Verify explainability request rejects invalid gas label | `gas=so2` | HTTP `400`, invalid gas type message | Pending execution | Pending Endpoint Activation |
| BB-XAI-003 | Verify explainability response structure is aligned with model inputs | Valid request | All expected features are present and feature names are interpretable | Pending execution | Pending Endpoint Activation |
| BB-XAI-004 | Verify explainability magnitude is logically bounded | Valid request | Contribution values are finite, non-null, and sum approximately to the prediction delta after normalization | Pending execution | Pending Endpoint Activation |

### 3.4 Data Visualization and Dashboard Updates

| Test Case ID | Description | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| BB-VIS-001 | Verify dashboard updates when historical filters change | Change region, sector, gas, start year, and end year then click `Update Data` | Line chart, gas composition chart, top subsector metrics, and insights panel update to new selection | Pending execution | Not Executed |
| BB-VIS-002 | Verify prediction page updates after generating a new forecast | Change forecast configuration and click `Generate forecasts` | Prediction charts and summary cards update to the latest request | Pending execution | Not Executed |
| BB-VIS-003 | Verify monthly chart handles short or incomplete data safely | Forecast response with fewer than 12 monthly values | Missing months are safely padded and chart still renders | Pending execution | Not Executed |
| BB-VIS-004 | Verify no-data state is shown when visualization payload is empty | Empty `yearly_totals` or empty prediction object | User sees informative placeholder instead of broken chart component | Pending execution | Not Executed |
| BB-VIS-005 | Verify heatmap asset is displayed | Open dashboard visualization panel | Heatmap image loads successfully; if image is missing, fallback message appears | Pending execution | Not Executed |

### 3.5 CSV Download and Data Export

| Test Case ID | Description | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| BB-DL-001 | Verify data fetch succeeds for valid filter set | `region=pak`, `gas=co2`, `startYear=2020`, `endYear=2024` | HTTP `200`, preview table and row count displayed | Pending execution | Not Executed |
| BB-DL-002 | Verify year boundary validation on frontend | `startYear=2025`, `endYear=2020` | Frontend blocks request and shows `Start year cannot be greater than end year` | Pending execution | Not Executed |
| BB-DL-003 | Verify backend rejects missing year parameters | Missing `startYear` or `endYear` | HTTP `400`, message `startYear and endYear are required` | Pending execution | Not Executed |
| BB-DL-004 | Verify backend rejects non-integer years | `startYear=twenty`, `endYear=2024` | HTTP `400`, message indicating invalid integer values | Pending execution | Not Executed |
| BB-DL-005 | Verify backend rejects reversed year range | `startYear=2024`, `endYear=2020` | HTTP `400`, message `startYear must be less than or equal to endYear` | Pending execution | Not Executed |
| BB-DL-006 | Verify `n2o` filter is normalized to internal gas code | `gas=n2o` | Backend translates to internal gas label and still returns dataset correctly | Pending execution | Not Executed |
| BB-DL-007 | Verify CSV file generation after successful preview | Click `Download CSV` after successful fetch | Browser downloads a `.csv` file with correct headers and selected filter values in filename | Pending execution | Not Executed |
| BB-DL-008 | Verify export workflow handles empty result set | Valid filters returning zero rows | User sees `No data available for the selected filters`; no application crash | Pending execution | Not Executed |

## 4. White-Box Testing

### 4.1 Coverage Objectives

The white-box test suite aims to achieve:

- **Branch coverage** for authentication validation, route guards, gas normalization, and error handling branches
- **Condition coverage** for field presence checks, year comparison checks, login credential checks, and token validation checks
- **Path testing** for end-to-end controller paths such as `valid request -> DB lookup -> aggregation -> response` and `invalid request -> early return`

### 4.2 Automated Test Artifacts Added

- Backend route tests: [`Backend/tests/user.routes.test.js`](/d:/FYP/Backend/tests/user.routes.test.js), [`Backend/tests/data.routes.test.js`](/d:/FYP/Backend/tests/data.routes.test.js), [`Backend/tests/historical.routes.test.js`](/d:/FYP/Backend/tests/historical.routes.test.js)
- Backend Jest configuration: [`Backend/jest.config.js`](/d:/FYP/Backend/jest.config.js)
- Frontend component tests: [`Frontend/src/__tests__/AuthModal.test.jsx`](/d:/FYP/Frontend/src/__tests__/AuthModal.test.jsx), [`Frontend/src/__tests__/ForecastsConfiguration.test.jsx`](/d:/FYP/Frontend/src/__tests__/ForecastsConfiguration.test.jsx), [`Frontend/src/__tests__/DataDownload.test.jsx`](/d:/FYP/Frontend/src/__tests__/DataDownload.test.jsx), [`Frontend/src/__tests__/Prediction.integration.test.jsx`](/d:/FYP/Frontend/src/__tests__/Prediction.integration.test.jsx)
- Frontend Vitest configuration: [`Frontend/vitest.config.js`](/d:/FYP/Frontend/vitest.config.js), [`Frontend/src/test/setup.js`](/d:/FYP/Frontend/src/test/setup.js)
- Model unit tests: [`Model/tests/conftest.py`](/d:/FYP/Model/tests/conftest.py), [`Model/tests/test_preprocessing.py`](/d:/FYP/Model/tests/test_preprocessing.py), [`Model/tests/test_inference.py`](/d:/FYP/Model/tests/test_inference.py)

### 4.3 White-Box Test Design Summary

#### Backend

- Authentication tests cover successful signup/login, invalid credentials, refresh-token renewal, missing token, logout, and history persistence
- Data export tests cover all validation branches, including missing years, non-integer years, reversed year ranges, and successful SQL row normalization
- Historical analytics tests cover required-field validation, missing country/gas branches, aggregation logic, gas-ratio generation, and LLM insight fallback behavior

#### Frontend

- Authentication modal tests verify login flow, sign-up validation, and callback execution
- Forecast configuration tests verify that dropdown selections are converted into the correct request payload
- Data download tests verify year-range validation, backend request construction, preview rendering, and CSV download initiation
- Prediction integration tests verify the complete client workflow `page load -> prediction API call -> history API call -> chart section render`

#### Model

- Preprocessing tests verify both coordinate paths: explicit latitude/longitude and default fallback coordinates
- Inference tests verify the aggregation path across one or more subsectors and confirm monthly and total emissions are computed correctly

## 5. Integration Testing

### 5.1 Integration Objectives

The integration suite validates collaboration among major subsystems:

- Frontend to backend APIs for authentication, history, historical analytics, and data download
- Frontend to model API for forecast generation
- Backend to MongoDB for users and history
- Backend to PostgreSQL for historical and downloadable emissions data

### 5.2 Integration Workflows

| Integration ID | Workflow | Test Objective | Expected Result |
|---|---|---|---|
| INT-001 | `Login -> Dashboard historical request -> History saved -> Charts updated` | Validate frontend/backend/auth/database coordination | User logs in, dashboard data loads, MongoDB history entry is created, and charts update without errors |
| INT-002 | `Prediction page load -> Model API predict -> Backend history save -> Prediction UI render` | Validate prediction workflow across frontend, model API, and backend history API | Prediction payload is returned, history is stored, and prediction cards/charts render |
| INT-003 | `Data download filter selection -> Backend SQL query -> Preview table -> CSV export` | Validate download workflow from UI to PostgreSQL-backed API | Preview row set matches filters and CSV export is generated from preview data |
| INT-004 | `Historical request -> PostgreSQL aggregation -> Gemini insight generation -> Dashboard insight panel` | Validate analytical response composition | Historical totals, gas ratios, and textual insight block are returned in one coherent response |
| INT-005 | `Explainability request -> Feature attribution module -> UI explanation card` | Validate explainability integration when endpoint is enabled | Attribution output is returned and displayed with readable labels |

### 5.3 Implementation Note

The current codebase directly integrates the prediction page with the Flask model API rather than proxying forecast requests through Express. Therefore, the practical integration path is:

- `Frontend -> Flask Model API`
- `Frontend -> Express Backend`

If the architecture is later changed to `Frontend -> Backend -> Model API`, the same test cases remain valid, but the backend test layer should additionally mock outbound HTTP calls to the model service.

## 6. Regression Testing

### 6.1 Recommended Regression Suite

The regression suite should include the following high-priority scenarios:

- Successful signup, login, refresh token, and logout
- Failed login with invalid password
- Dashboard filter update and chart refresh
- Prediction request for each gas type: `co2`, `ch4`, `n2o`
- Data download preview and CSV export
- History write/read workflow for both historical and prediction pages
- Historical analytics ratio calculation and top subsector identification
- Error handling for missing fields and invalid years

### 6.2 When Regression Testing Should Be Run

Regression testing should be executed:

- After adding any new feature
- After fixing a defect in auth, prediction, download, charting, or database logic
- Before deployment to a demonstration or production environment
- After environment-variable or infrastructure changes
- After retraining or replacing the prediction model

## 7. Usability Testing

### 7.1 Usability Evaluation Method

Usability testing should involve 5-10 representative users such as students, supervisors, domain reviewers, or NGO/policy stakeholders. Each participant should complete common tasks and then submit structured feedback.

### 7.2 Sample Task Set

- Create a new account and sign in
- Retrieve historical emissions for a selected country and sector
- Generate a future emission forecast
- Interpret the chart outputs and gas distribution
- Download filtered data in CSV format

### 7.3 Structured Feedback Form

| Section | Question | Scale / Response Type |
|---|---|---|
| Learnability | How easy was it to understand the purpose of the system on first use? | 1 to 5 Likert |
| Navigation | How easy was it to move between dashboard, prediction, and download pages? | 1 to 5 Likert |
| Form Clarity | Were the dropdown labels and filter names clear? | 1 to 5 Likert |
| Feedback | Were loading states, errors, and success messages sufficiently clear? | 1 to 5 Likert |
| Visualization | How understandable were the charts and gas composition displays? | 1 to 5 Likert |
| Data Download | Was the export process simple and reliable? | 1 to 5 Likert |
| Trust | Did the predicted values and insights appear believable and well explained? | 1 to 5 Likert |
| Efficiency | How quickly could you complete the assigned tasks? | Short text |
| UI Issues | Which visual or usability issues did you encounter? | Short text |
| Improvement Suggestions | What changes would most improve the system? | Short text |

### 7.4 Usability Metrics

- Task completion rate
- Average completion time per task
- Number of user errors per task
- Post-test satisfaction score
- Number of critical UI issues reported

## 8. Validation Testing

### 8.1 Prediction Validation

The prediction model should be validated using both technical and logical criteria:

- Compare model predictions against a hold-out validation dataset using MAE, RMSE, and MAPE
- Verify that emissions are non-negative for all forecast months
- Confirm that `total_emissions` is equal to the sum of `monthly_trends` within a small tolerance
- Confirm that the total forecast equals the sum of all subsector totals within a small tolerance
- Check that future predictions do not show impossible discontinuities without corresponding explanatory features
- Compare forecasts across gases and sectors to ensure relative magnitudes remain domain-plausible

### 8.2 Explainability Validation

For SHAP-style or feature-attribution outputs, the following checks should be applied:

- Feature labels must correspond exactly to actual model input features
- The number of attribution values must match the number of model features
- Attribution values must be finite numeric values with no `NaN` or `Infinity`
- The sign of feature contribution should align with domain logic where possible
- The sum of feature contributions plus baseline should approximately reconstruct the predicted value
- Similar input samples should not produce radically inconsistent attribution profiles without a valid data reason

### 8.3 Logical Consistency Checks

| Validation ID | Consistency Rule | Acceptance Criterion |
|---|---|---|
| VAL-001 | `sum(monthly_trends) ≈ total_emissions` | Difference within predefined numerical tolerance |
| VAL-002 | `sum(subsector totals) ≈ total_emissions` | Difference within predefined numerical tolerance |
| VAL-003 | `sum(gas ratios)` | Approximately `100%` or `1.0` depending on representation |
| VAL-004 | Gas totals are non-negative | All values `>= 0` |
| VAL-005 | Historical yearly totals equal subsector aggregation | Recomputed totals match API response |
| VAL-006 | Explainability vector length matches feature count | Exact match |

## 9. Performance Testing (Bonus)

### 9.1 Load Testing Strategy

The prediction API is the most computationally sensitive module and should be evaluated under concurrent access. A practical performance testing plan is:

- Use `k6`, JMeter, or Locust to simulate concurrent users
- Start with `10` virtual users and gradually increase to `25`, `50`, and `100`
- Use realistic forecast requests covering multiple countries, sectors, and gas types
- Measure average response time, 95th percentile latency, error rate, CPU usage, and memory usage
- Record the point at which prediction latency degrades beyond acceptable threshold

### 9.2 Suggested Performance Targets

- Average prediction API response time: less than `2.0 seconds` under `25` concurrent users
- 95th percentile response time: less than `4.0 seconds`
- Error rate: less than `1%`
- Dashboard and download APIs should remain responsive while prediction requests are under load

## 10. Test Execution Guidance

### 10.1 Backend

Suggested tooling:

```bash
npm install --save-dev jest supertest
```

Suggested execution:

```bash
set NODE_OPTIONS=--experimental-vm-modules
npx jest --config jest.config.js --coverage
```

### 10.2 Frontend

Suggested tooling:

```bash
npm install --save-dev vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

Suggested execution:

```bash
npx vitest run --coverage
```

### 10.3 Model

Suggested tooling:

```bash
pip install pytest
```

Suggested execution:

```bash
pytest Model/tests -q
```

## 11. Conclusion

This testing suite provides a comprehensive quality-assurance framework for the GHG Emissions Forecasting System. It addresses:

- Functional correctness through black-box testing
- Internal logic verification through white-box testing
- Subsystem collaboration through integration testing
- Ongoing software stability through regression testing
- User-centered quality through usability testing
- ML soundness through validation testing
- Scalability considerations through performance testing

As a final year project deliverable, this suite is suitable for academic submission and can also serve as a practical foundation for future industrial-level QA expansion.

## 12. Observed Failed Cases

The automated unit and integration-style tests are expected to pass when the code is behaving correctly. However, for academic reporting it is also important to present genuine limitations or failed cases found during review. The following are real issues in the current project:

| Issue ID | Area | Observation | Evidence | Status |
|---|---|---|---|---|
| FAIL-001 | Explainability API | The project contains explainability logic, but the `/api/explain` route is currently commented out, so explainability cannot be tested end-to-end from the running API. | [`Model/app.py`](/d:/FYP/Model/app.py) | Failed / Needs Implementation |
| FAIL-002 | Validation Consistency | The signup UI text says password must be at least 8 characters, but backend validation accepts 6 characters. This creates inconsistent behavior between frontend expectation and backend rule. | [`Frontend/src/Pages/AuthModal.jsx`](/d:/FYP/Frontend/src/Pages/AuthModal.jsx), [`Backend/src/controllers/user.controlers.js`](/d:/FYP/Backend/src/controllers/user.controlers.js), [`Backend/src/models/user.model.js`](/d:/FYP/Backend/src/models/user.model.js) | Failed / Needs Alignment |
