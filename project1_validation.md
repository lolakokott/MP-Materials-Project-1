# Project 1 — Validation Record

## 1. Known-Answer Reconciliation

I tested the original pro-forma engine against the ABG known-answer exercise from Lab 09.

The model reproduced the following expected results:

| Metric | Expected | Actual |
|---|---:|---:|
| FY2026 Revenue ($M) | 18,323.0 | 18,323.0 |
| FY2030 Revenue ($M) | 19,678.3 | 19,678.3 |
| FY2026 FCFE ($M) | 211.4 | 211.4 |
| FY2030 FCFE ($M) | 342.3 | 342.3 |
| FY2026 Cash ($M) | 101.8 | 101.8 |
| FY2030 Cash ($M) | 719.8 | 719.8 |

**Result:** PASS — the original engine reproduces the recorded Lab 09 known-answer results.

## 2. Failure Detection

During Lab 09, I intentionally introduced an incorrect FY2026 cash balance. The model detected a balance sheet gap of -$61.4 million and rejected the result.

**Result:** PASS — the original engine detected the intentional accounting discrepancy.

## 3. MP Materials Validation

The updated MP Materials model includes annual balance sheet and liquidity checks for 2026–2030.

I also completed a locked changed-input test, increasing gross margin from 14.1% to 15.1%. Operating income and FCFF increased, and the accounting/liquidity checks passed.

The downside investment scenario failed its FY2030 minimum cash requirement, demonstrating a financing limitation.

**Limitations:** The original ABG validation does not independently verify every modification to the MP Materials model. Additional source reconciliation, cash-flow tie-out, valuation checks, and a clean-environment run are required.

## 4. Supporting Evidence

- `validation_abg.txt` — original engine output
- `locked_changed_input.md` — precommitted prediction and actual results
- `project1_results.txt` — integrated DCF, sensitivities, and scenarios
- `project1_model.py` — MP Materials three-statement model
- `project1_dcf.py` — integrated FCFF valuation

## 5. Cash Flow Reconciliation

I independently tested whether projected cash flows reconcile
to the balance sheet's ending cash balance.

For each year from 2026–2030, I calculated:

Ending Cash = Opening Cash + Operating Cash Flow
              + Investing Cash Flow + Financing Cash Flow

Results:
- FY2026: PASS
- FY2027: PASS
- FY2028: PASS
- FY2029: PASS
- FY2030: PASS

All five years had a reconciliation gap of approximately
$0.000000 million.

Evidence: project1_cashflow_checks.txt

## 6. Independent Source Check

Input: Opening cash and short-term investments
Source: MP Materials 2025 Form 10-K, p. 124

Reported cash: $1,166.011M
Reported short-term investments: $664.275M
Combined amount: $1,830.286M
Model input: $1,830.286M

Result: PASS — historical input matches the filing.

Limitation: Combining these accounts does not mean all
funds are freely available for future expansion.