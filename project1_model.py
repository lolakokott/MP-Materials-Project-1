"""Lab 10: MP Materials through the Lab 09 engine (USD millions).

Run: python3 mp_proforma.py
Operating judgments: lab10.md, Forecast Assumptions.
Opening history: MP-research/mp-10k2026.pdf, PDF pp. 124 and 173.
Revolver capacity: same filing, PDF p. 102. Shares: PDF p. 124.

This is a simplified classroom model, not a complete MP valuation. It retains
Lab 09's structure; it does not separately forecast PPA income, customer advances,
non-PP&E amortization, preferred conversion, or contractual covenant tests.
NdPr volume is a documented operating KPI, not a second revenue multiplier.
Missing nonoperating settings retain explicit Lab 09 classroom defaults below.
Cash includes short-term investments. Preferred stock is a fixed separate claim.
Financing failures stop valuation; negative FCFE is retained in the statements.
"""

import math
from copy import deepcopy


# Judgment: lab10.md values are used as written, including displayed rounding.
YEARS = range(2026, 2031)
GROWTH = 0.10
GROSS_MARGIN = 0.1410  # Pre-DD&A profit proxy, not reported gross margin.
SGA_RATIOS = (3.5406,) * 5
DEPRECIATION_RATIO = 0.0556
INVENTORY_DAYS = 325.0
CAPEX = (550.0, 206.897, 206.897, 206.897, 206.897)
TAX_RATE = 0.28
NDPR_SALES_VOLUME = (2500, 3000, 3500, 4000, 4500)  # Metric tons, 2026-2030.
FLOOR_PLAN_RATIO = 0.0  # Judgment: none / not applicable.
FLOOR_PLAN_RATE = 0.0
IMPAIRMENT = 0.0  # Judgment: no scheduled ABG impairment.
REPAYMENT = 0.0  # Judgment: no net repayment; assumes maturities refinanced.
BUYBACK = 0.0  # Judgment: preserve cash during expansion and losses.
NEW_DEBT_2030 = 300.0  # Judgment: fund the $266.25m shortfall with a cushion.
# Additional to refinancing; not committed financing or management guidance.
# Opening-balance interest convention: interest on this borrowing starts in 2031.

# Retained Lab 09 classroom judgments: not supplied by lab10.md or MP guidance.
# OTHER_WC_RATIO: keep the engine's small incremental working-capital allowance.
# MINIMUM_CASH: keep its simple liquidity buffer, not MP's contractual covenant.
# Rates: retain the original financing/valuation assumptions without market research.
OTHER_WC_RATIO = 0.008
MINIMUM_CASH = 25.0
REVOLVER_RATE = 0.06
DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025

# History: remaining borrowing capacity at December 31, 2025.
# Judgment: assume this ceiling is available throughout the annual forecast;
# actual covenants and the August 2030 maturity are not modeled here.
REVOLVER_LIMIT = 235.0
# History: year-end shares. Judgment: keep fixed; no incremental dilution.
SHARES = 177.357647
TOLERANCE = 1e-8

# History: December 31, 2025 balances, grouped for the existing engine.
# cash = 1166.011 cash + 664.275 short-term investments.
# debt = 998.741 balance-sheet debt + 24.270 equipment notes.
# other_liabilities = 1471.792 total liabilities - 1023.011 debt.
# other_assets = 3864.160 total assets - cash - current inventory - PP&E.
# Judgment: preferred book value remains fixed, separate from common equity.
OPENING = dict(
    revenue=224.441, inventory=171.560, ppe=1369.817,
    other_assets=492.497, cash=1830.286, floor_plan=0.0,
    debt=1023.011, other_liabilities=448.781, equity=1978.757,
    preferred=413.611, revolver=0.0,
)


# Independent assumptions only; linked statement quantities are recalculated.
BASE_INPUTS = {
    "opening": deepcopy(OPENING),
    "annual": {},
    "valuation": {"COST_OF_EQUITY": COST_OF_EQUITY,
                  "TERMINAL_GROWTH": TERMINAL_GROWTH, "SHARES": SHARES},
}
for _index, _year in enumerate(YEARS):
    BASE_INPUTS["annual"][_year] = {
        "GROWTH": GROWTH,
        "GROSS_MARGIN": GROSS_MARGIN,
        "DEPRECIATION_RATIO": DEPRECIATION_RATIO,
        "INVENTORY_DAYS": INVENTORY_DAYS,
        "TAX_RATE": TAX_RATE,
        "FLOOR_PLAN_RATIO": FLOOR_PLAN_RATIO,
        "FLOOR_PLAN_RATE": FLOOR_PLAN_RATE,
        "IMPAIRMENT": IMPAIRMENT,
        "REPAYMENT": REPAYMENT,
        "BUYBACK": BUYBACK,
        "OTHER_WC_RATIO": OTHER_WC_RATIO,
        "MINIMUM_CASH": MINIMUM_CASH,
        "REVOLVER_RATE": REVOLVER_RATE,
        "DEBT_RATE": DEBT_RATE,
        "REVOLVER_LIMIT": REVOLVER_LIMIT,
        "SGA_RATIO": SGA_RATIOS[_index], "CAPEX": CAPEX[_index],
        "NDPR_SALES_VOLUME": NDPR_SALES_VOLUME[_index],
        "NEW_DEBT": NEW_DEBT_2030 if _year == 2030 else 0.0,
    }


def fresh_base_inputs():
    """Return an independent deep copy; never mutate BASE_INPUTS during a run."""
    return deepcopy(BASE_INPUTS)


def project(inputs=None):
    """Recalculate all linked statements from an independent input copy."""
    inputs = fresh_base_inputs() if inputs is None else deepcopy(inputs)
    opening = inputs["opening"].copy()
    results = []
    for year in YEARS:
        assumptions = inputs["annual"][year]
        sga_ratio = assumptions["SGA_RATIO"]
        capex = assumptions["CAPEX"]
        ndpr_volume = assumptions["NDPR_SALES_VOLUME"]
        row = {"year": year, "ndpr_volume": ndpr_volume}
        
        # MP-specific revenue drivers: NdPr sales and other products
        ndpr_price_per_kg = 60.0  # Analyst assumption
        other_revenue_by_year = {
            2026: 80.0,
            2027: 90.0,
            2028: 100.0,
            2029: 110.0,
            2030: 120.0,
        }

        row["revenue"] = (
            ndpr_volume * ndpr_price_per_kg / 1000
            + other_revenue_by_year[year]
        )

        row["gross_profit"] = row["revenue"] * assumptions["GROSS_MARGIN"]
        row["cogs"] = row["revenue"] - row["gross_profit"]
        row["sga"] = 112.066 * (1.03 ** (year - 2026))
        row["depreciation"] = opening["ppe"] * assumptions["DEPRECIATION_RATIO"]
        row["impairment"] = assumptions["IMPAIRMENT"]
        row["operating_income"] = (
            row["gross_profit"] - row["sga"]
            - row["depreciation"] - row["impairment"]
        )
        row["interest"] = (
            opening["floor_plan"] * assumptions["FLOOR_PLAN_RATE"]
            + opening["debt"] * assumptions["DEBT_RATE"]
            + opening["revolver"] * assumptions["REVOLVER_RATE"]
        )
        row["pretax"] = row["operating_income"] - row["interest"]
        row["tax"] = max(0.0, row["pretax"]) * assumptions["TAX_RATE"]
        row["net_income"] = row["pretax"] - row["tax"]

        row["inventory"] = row["cogs"] * assumptions["INVENTORY_DAYS"] / 365
        row["floor_plan"] = row["inventory"] * assumptions["FLOOR_PLAN_RATIO"]
        row["capex"] = capex
        row["ppe"] = opening["ppe"] + capex - row["depreciation"]
        row["change_other_wc"] = (
            assumptions["OTHER_WC_RATIO"] * (row["revenue"] - opening["revenue"])
        )
        row["other_assets"] = (
            opening["other_assets"] + row["change_other_wc"] - assumptions["IMPAIRMENT"]
        )
        row["repayment"] = assumptions["REPAYMENT"]
        row["new_debt"] = assumptions["NEW_DEBT"]
        row["debt"] = opening["debt"] + row["new_debt"] - assumptions["REPAYMENT"]
        row["other_liabilities"] = opening["other_liabilities"]
        row["preferred"] = opening["preferred"]
        row["buyback"] = assumptions["BUYBACK"]
        row["equity"] = opening["equity"] + row["net_income"] - assumptions["BUYBACK"]
        row["change_inventory"] = row["inventory"] - opening["inventory"]
        row["change_floor_plan"] = row["floor_plan"] - opening["floor_plan"]
        # Unlevered free cash flow to the firm (FCFF)
        row["fcff"] = (
            row["operating_income"]
            - max(0.0, row["operating_income"]) * assumptions["TAX_RATE"]
            + row["depreciation"]
            + row["impairment"]
            - row["capex"]
            - row["change_inventory"]
            - row["change_other_wc"]
            )
        # Other WC is the revenue-driven addition, excluding noncash impairment.
        row["fcfe"] = (
            row["net_income"] + row["depreciation"] + assumptions["IMPAIRMENT"] - capex
            - row["change_inventory"] - row["change_other_wc"]
            + row["change_floor_plan"] + row["new_debt"] - assumptions["REPAYMENT"]
        )
        cash_before_revolver = opening["cash"] + row["fcfe"] - assumptions["BUYBACK"]
        if cash_before_revolver < assumptions["MINIMUM_CASH"]:
            row["change_revolver"] = min(
                assumptions["MINIMUM_CASH"] - cash_before_revolver,
                assumptions["REVOLVER_LIMIT"] - opening["revolver"],
            )
        else:
            row["change_revolver"] = -min(
                cash_before_revolver - assumptions["MINIMUM_CASH"], opening["revolver"]
            )
        row["revolver"] = opening["revolver"] + row["change_revolver"]
        row["opening_cash"] = opening["cash"]
        row["cash"] = cash_before_revolver + row["change_revolver"]
        row["change_cash"] = row["cash"] - opening["cash"]
        row["assets"] = sum(row[k] for k in (
            "inventory", "ppe", "other_assets", "cash"
        ))
        row["liabilities"] = sum(row[k] for k in (
            "floor_plan", "debt", "revolver", "other_liabilities"
        ))
        row["liabilities_equity"] = (
            row["liabilities"] + row["preferred"] + row["equity"]
        )
        row["balance_gap"] = row["assets"] - row["liabilities_equity"]
        row["cash_headroom"] = row["cash"] - assumptions["MINIMUM_CASH"]
        row["cash_ok"] = row["cash_headroom"] >= -TOLERANCE
        row["minimum_cash"] = assumptions["MINIMUM_CASH"]
        row["revolver_limit"] = assumptions["REVOLVER_LIMIT"]
        results.append(row)
        opening = row
    return results


def assert_balanced(results):
    """Raise with the year and gap for a failed balance or liquidity check."""
    for row in results:
        gap = row["balance_gap"]
        if not math.isfinite(gap) or abs(gap) > TOLERANCE:
            raise ValueError(f"FY{row['year']}: balance sheet gap = {gap:.10f}")
        gap = row["cash_headroom"]
        if not math.isfinite(gap) or gap < -TOLERANCE:
            raise ValueError(f"FY{row['year']}: cash minus minimum gap = {gap:.10f}")
        revolver = row["revolver"]
        limit = row.get("revolver_limit", REVOLVER_LIMIT)
        if not math.isfinite(revolver) or not -TOLERANCE <= revolver <= limit + TOLERANCE:
            gap = revolver if revolver < 0 else revolver - limit
            raise ValueError(f"FY{row['year']}: revolver bound gap = {gap:.10f}")


def print_table(title, results, fields, units="USD millions"):
    print(f"\n{title} ({units})")
    print(f"{'':36}" + "".join(f"{'FY' + str(r['year']) + 'E':>14}" for r in results))
    for label, key, sign in fields:
        values = []
        for row in results:
            value = row[key] * sign
            if abs(value) < 0.05:
                value = 0.0  # Avoid displaying negative zero.
            values.append(f"{value:14,.1f}")
        print(f"{label:36}" + "".join(values))


def main():
    print("MP Materials — simplified Lab 10 scenario; assumptions in lab10.md.")
    print("Retained Lab 09 rate and liquidity settings are classroom judgments.")
    print("Gross profit is a pre-DD&A proxy; floor-plan financing is not applicable.")
    results = project()
    print_table("COMPANY-SPECIFIC OPERATING LINE", results, [
        ("NdPr sales volume", "ndpr_volume", 1),
    ], units="metric tons of NdPr oxide equivalent")
    print("NdPr volume replaces the same-store concept; revenue still grows by 10%.")
    print_table("INCOME STATEMENT", results, [
        ("Revenue", "revenue", 1), ("Cost of sales, excluding DD&A", "cogs", -1),
        ("Gross profit proxy, before DD&A", "gross_profit", 1), ("SG&A", "sga", -1),
        ("Depreciation", "depreciation", -1), ("Impairment", "impairment", -1),
        ("Operating income", "operating_income", 1), ("Interest", "interest", -1),
        ("Pretax income", "pretax", 1), ("Tax", "tax", -1),
        ("Net income", "net_income", 1),
    ])
    print_table("BALANCE SHEET", results, [
        ("Cash", "cash", 1), ("Inventory", "inventory", 1),
        ("PP&E", "ppe", 1), ("Other assets", "other_assets", 1),
        ("Total assets", "assets", 1), ("Floor plan", "floor_plan", 1),
        ("Term debt", "debt", 1), ("Revolver", "revolver", 1),
        ("Other liabilities", "other_liabilities", 1),
        ("Total liabilities", "liabilities", 1),
        ("Redeemable preferred stock", "preferred", 1), ("Common equity", "equity", 1),
        ("Liabilities + preferred + equity", "liabilities_equity", 1),
    ])
    print_table("CASH FLOW", results, [
        ("Net income", "net_income", 1), ("Depreciation addback", "depreciation", 1),
        ("Impairment addback", "impairment", 1), ("Capital spending", "capex", -1),
        ("Inventory increase", "change_inventory", -1),
        ("Other working capital increase", "change_other_wc", -1),
        ("Floor plan increase", "change_floor_plan", 1),
        ("New long-term borrowing", "new_debt", 1),
        ("Term debt repayment", "repayment", -1),
        ("FCFE", "fcfe", 1),
        ("Unlevered FCFF", "fcff", 1),
        ("Share buyback", "buyback", -1),
        ("Revolver draw / (repayment)", "change_revolver", 1),
        ("Change in cash", "change_cash", 1), ("Opening cash", "opening_cash", 1),
        ("Closing cash", "cash", 1),
    ])
    print_table("ANNUAL CHECKS", results, [
        ("Assets - liabilities - pref - equity", "balance_gap", 1),
        ("Cash minus minimum", "cash_headroom", 1),
    ])
    print(f"{'Cash at or above minimum':36}" + "".join(
        f"{'PASS' if row['cash_ok'] else 'FAIL':>14}" for row in results
    ))
    for row in results:
        status = "negative FCFE" if row["fcfe"] < 0 else "nonnegative FCFE"
        print(f"FY{row['year']}: {status} = ${row['fcfe']:,.3f} million")
    assert_balanced(results)

    # Lab 10: value only positive cash flows; do not erase statement losses.
    pv_fcfe = sum(max(0.0, row["fcfe"]) / (1 + COST_OF_EQUITY) ** t
                  for t, row in enumerate(results, 1))
    last = results[-1]
    terminal_cash_flow = last["fcfe"] + last["repayment"]
    if last["fcfe"] <= 0 or terminal_cash_flow <= 0:
        terminal_value = 0.0
        print("No terminal value: terminal FCFE is nonpositive.")
        print("Growing negative cash flow forever is not a meaningful terminal value.")
    else:
        if COST_OF_EQUITY <= TERMINAL_GROWTH:
            raise ValueError("Discount rate must exceed terminal growth.")
        terminal_value = (terminal_cash_flow * (1 + TERMINAL_GROWTH)
                          / (COST_OF_EQUITY - TERMINAL_GROWTH))
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** len(results)
    equity_value = pv_fcfe + pv_terminal
    print(f"\nClassroom equity value (USD millions): ${equity_value:,.2f}")
    if equity_value == 0:
        print("Share of value after 2030: N/A (zero equity value)")
    else:
        print(f"Share of value after 2030: {pv_terminal / equity_value:.2%}")
    print(f"Value per share (simplified Lab 10): ${equity_value / SHARES:,.2f}")
    print("This engine does not separately value preferred or conversion rights.")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"REFUSED: {error}. No value per share issued.")
