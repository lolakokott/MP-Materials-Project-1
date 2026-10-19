# Project 1 — MP Materials Corporate Finance Application

**Course:** FIN 43900 — AI in Finance  
**Company:** MP Materials Corp. (NYSE: MP)  
**Recommendation:** WATCH / DEFER  
**Forecast Period:** 2026–2030  
**Currency:** USD millions unless otherwise noted

## Project Overview

This project evaluates whether an investment fund should initiate a position in MP Materials. The analysis combines historical financial research, a five-year three-statement pro-forma, an FCFF DCF, comparable-company analysis, sensitivity testing, and validation.

The recommendation is to defer investing until there is stronger evidence supporting future profitability and financing requirements.

## How to Run

The project uses Python 3 and standard-library dependencies.

From the `MP-research` directory, run:

```bash
python3 project1_model.py
python3 project1_dcf.py
python3 project1_sensitivity.py
```

These programs generate financial projections, discounted cash flow calculations, valuation sensitivities, and operating scenarios.

### Interactive Streamlit Application

The project also includes an interactive application for adjusting assumptions, reviewing valuation results, and testing model validation checks.

To launch the application, install Streamlit if needed:

```bash
python3 -m pip install streamlit

## Main Files

| File | Purpose |
|---|---|
| `project1_model.py` | Five-year financial statements |
| `project1_dcf.py` | Integrated FCFF DCF, reverse DCF, and scenarios |
| `project1_sensitivity.py` | Gross-margin and capital-spending tests |
| `project1_results.txt` | Saved valuation outputs |
| `project1_comparables.md` | Peer policy and valuation multiples |
| `project1_memo.md` | Investment committee recommendation |
| `project1_validation.md` | Validation and testing summary |
| `project1_reconciliation.md` | Historical financial reconciliation |
| `locked_changed_input.md` | Precommitted prediction and actual results |
| `project1_cashflow_checks.txt` | Cash flow reconciliation results |
| `project1_cold_run.txt` | Fresh-environment execution log |
| `validation_abg.txt` | Original known-answer training-case output |
| project1_app.py | Interactive Streamlit valuation and validation application |

## Valuation Results

The integrated DCF uses an 11% WACC and 3% terminal growth rate.

| Scenario | Preliminary Enterprise Value |
|---|---:|
| Downside | -$1,244.15M |
| Base | -$1,108.79M |
| Upside | -$973.43M |

The downside scenario fails its modeled liquidity requirement. These figures are diagnostic enterprise values, not common-share price estimates.

The analysis supports WATCH / DEFER because the modeled operating performance and financing assumptions do not establish a reliable positive common-equity valuation.

## Validation

Testing includes balance-sheet checks, cash flow reconciliation, an ABG training-case comparison, a locked changed-input test, operating sensitivities, and a clean-environment run.

Refer to the validation files for results and limitations.

## Key Limitations

The model simplifies MP Materials' expansion, government agreements, financing, dilution, and terminal profitability. Some market and financial-statement inputs have different observation dates.

The conclusions are conditional on the documented assumptions and are not investment advice.

## Research Sources

MP Materials FY2025 Form 10-K, Q2 2026 financial disclosures, and historical market information. Additional source references appear in the research and valuation documents.