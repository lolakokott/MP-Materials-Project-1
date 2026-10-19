# Project 1 — Historical Financial Reconciliation

**Company:** MP Materials Corp.  
**Base year:** December 31, 2025  
**Source:** MP Materials FY2025 Form 10-K, Consolidated Financial Statements, PDF p. 124 and related debt disclosures.  
**Units:** USD millions

## Historical Inputs

| Financial Item | 2025 Filing | Model Input |
|---|---:|---:|
| Revenue | 224.441 | 224.441 |
| Cash and short-term investments | 1,830.286 | 1,830.286 |
| Current inventory | 171.560 | 171.560 |
| Property, plant & equipment | 1,369.817 | 1,369.817 |
| Other assets (grouped) | 492.497 | 492.497 |
| Total assets | 3,864.160 | 3,864.160 |
| Debt including equipment notes | 1,023.011 | 1,023.011 |
| Other liabilities (grouped) | 448.781 | 448.781 |
| Preferred stock | 413.611 | 413.611 |
| Common equity | 1,978.757 | 1,978.757 |

## Reconciliation Method

The model groups certain balance-sheet categories while preserving the historical totals.

- Cash and investments = 1,166.011 + 664.275 = 1,830.286
- Debt = 998.741 + 24.270 equipment notes = 1,023.011
- Other assets = total assets less cash/investments, current inventory, and PP&E
- Other liabilities = total liabilities less modeled debt

Total assets = 3,864.160 million.

Total liabilities + preferred stock + common equity = 3,864.160 million.

**Balance-sheet difference: $0.000 million.**

## Conclusion

The opening model inputs reconcile to the FY2025 financial amounts identified in the company filing, using the grouping conventions described above. The modeled opening balance sheet balances.

These checks verify the historical starting point, not the reasonableness of future forecasts. Cash and short-term investments are combined for modeling purposes, but this does not mean all balances are available without restriction.