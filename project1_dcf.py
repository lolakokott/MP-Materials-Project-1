
"""Project 1: MP Materials integrated FCFF DCF.
Preliminary enterprise valuation; USD millions.
"""

import project1_model as model

WACC = 0.11
TERMINAL_GROWTH = 0.03
TERMINAL_MARGIN = 0.20
TERMINAL_TAX = 0.25
TERMINAL_ROIC = 0.12

# Obtain five-year forecasts directly from the pro-forma
results = model.project()
model.assert_balanced(results)

# Discount all FCFF, including negative years
pv_fcff = sum(
    row["fcff"] / (1 + WACC) ** t
    for t, row in enumerate(results, 1)
)

# Illustrative normalized 2031 terminal economics
# Assumptions carried from the earlier DCF.
revenue_2031 = results[-1]["revenue"] * (1 + TERMINAL_GROWTH)
nopat_2031 = revenue_2031 * TERMINAL_MARGIN * (1 - TERMINAL_TAX)
terminal_fcff = nopat_2031 * (1 - TERMINAL_GROWTH / TERMINAL_ROIC)

terminal_value = terminal_fcff / (WACC - TERMINAL_GROWTH)
pv_terminal = terminal_value / (1 + WACC) ** len(results)

enterprise_value = pv_fcff + pv_terminal

print("\nMP MATERIALS — INTEGRATED FCFF DCF")
print("---------------------------------")

for row in results:
    print(f"{row['year']}: FCFF = ${row['fcff']:,.2f}M")

print(f"\nWACC: {WACC:.1%}")
print(f"Terminal growth: {TERMINAL_GROWTH:.1%}")
print(f"PV of forecast FCFF: ${pv_fcff:,.2f}M")
print(f"PV of terminal value: ${pv_terminal:,.2f}M")
print(f"Preliminary enterprise value: ${enterprise_value:,.2f}M")

if enterprise_value < 0:
    print("WARNING: Negative modeled enterprise value.")
    print("Review operating assumptions, terminal transition,")
    print("and funding feasibility before deriving equity value.")


# WACC versus terminal growth sensitivity
print("\nWACC–TERMINAL GROWTH SENSITIVITY")
print("Enterprise value, USD millions")
print(f"{'WACC':>8} {'2%':>14} {'3%':>14} {'4%':>14}")

for wacc in [0.09, 0.11, 0.13]:
    values = []

    for growth in [0.02, 0.03, 0.04]:
        forecast_pv = sum(
            row["fcff"] / (1 + wacc) ** t
            for t, row in enumerate(results, 1)
        )

        future_revenue = results[-1]["revenue"] * (1 + growth)
        future_nopat = future_revenue * TERMINAL_MARGIN * (1 - TERMINAL_TAX)
        future_fcff = future_nopat * (1 - growth / TERMINAL_ROIC)

        future_terminal_value = future_fcff / (wacc - growth)
        discounted_terminal = future_terminal_value / (1 + wacc) ** len(results)

        ev = forecast_pv + discounted_terminal
        values.append(f"{ev:14,.2f}")

    print(f"{wacc:>7.0%} " + " ".join(values))


# Named investment scenarios
print("\nNAMED INVESTMENT SCENARIOS")
print("USD millions; illustrative assumptions")

cases = [
    ("Downside", 0.121, 1.10),
    ("Base", 0.141, 1.00),
    ("Upside", 0.161, 0.90),
]

for name, margin, capex_factor in cases:
    inputs = model.fresh_base_inputs()

    for year in model.YEARS:
        inputs["annual"][year]["GROSS_MARGIN"] = margin
        inputs["annual"][year]["CAPEX"] *= capex_factor

    forecast = model.project(inputs)

    try:
        model.assert_balanced(forecast)
        check_status = "PASS"
    except ValueError as error:
        check_status = f"FAIL: {error}"

    # Discount signed FCFF from the three-statement model
    forecast_pv = sum(
        row["fcff"] / (1 + WACC) ** t
        for t, row in enumerate(forecast, 1)
    )

    # Same provisional terminal assumptions as base DCF
    terminal_revenue = forecast[-1]["revenue"] * (1 + TERMINAL_GROWTH)
    terminal_nopat = terminal_revenue * TERMINAL_MARGIN * (1 - TERMINAL_TAX)
    terminal_fcff = terminal_nopat * (1 - TERMINAL_GROWTH / TERMINAL_ROIC)

    terminal_pv = (
        terminal_fcff / (WACC - TERMINAL_GROWTH)
        / (1 + WACC) ** len(forecast)
    )

    scenario_ev = forecast_pv + terminal_pv

    print(f"\n{name.upper()} CASE")
    print(f"Gross margin: {margin:.1%}")
    print(f"Capex multiplier: {capex_factor:.0%}")
    print(f"2030 operating income: ${forecast[-1]['operating_income']:,.2f}M")
    print(f"2030 FCFF: ${forecast[-1]['fcff']:,.2f}M")
    print(f"Conditional enterprise value: ${scenario_ev:,.2f}M")
    print(f"Accounting and liquidity: {check_status}")

    if check_status != "PASS":
        print("WARNING: Scenario exceeds modeled financing constraints.")

    if scenario_ev < 0:
        print("WARNING: Negative modeled EV; no reliable share value.")


# Enterprise-to-equity bridge — historical FY2025 basis
# Diagnostic only: carrying values, not market values.

print("\nENTERPRISE-TO-EQUITY BRIDGE")
print("December 2025 balance-sheet basis; USD millions")

cash = model.OPENING["cash"]
debt = model.OPENING["debt"] + model.OPENING["revolver"]
preferred = model.OPENING["preferred"]

common_equity_value = enterprise_value + cash - debt - preferred

print(f"Enterprise value: ${enterprise_value:,.2f}M")
print(f"Add cash and investments: ${cash:,.2f}M")
print(f"Less debt: ${debt:,.2f}M")
print(f"Less preferred stock: ${preferred:,.2f}M")
print(f"Residual common equity: ${common_equity_value:,.2f}M")

if enterprise_value <= 0 or common_equity_value <= 0:
    print("No defensible positive per-share value from this scenario.")
    print("Funding, dilution, and terminal economics require further review.")


# REVERSE DCF — illustrative market-implied expectation
# Historical quote from September 8, 2026.
# Uses FY2025 capital structure as a simplified reference.
# Date mismatch and dilution are important limitations.

market_price = 56.77

market_cap = market_price * model.SHARES

required_ev = (
    market_cap
    + model.OPENING["debt"]
    + model.OPENING["preferred"]
    - model.OPENING["cash"]
)

required_terminal_pv = required_ev - pv_fcff

required_terminal_fcff = (
    required_terminal_pv
    * (WACC - TERMINAL_GROWTH)
    * (1 + WACC) ** len(results)
)

required_margin = required_terminal_fcff / (
    results[-1]["revenue"]
    * (1 + TERMINAL_GROWTH)
    * (1 - TERMINAL_TAX)
    * (1 - TERMINAL_GROWTH / TERMINAL_ROIC)
)

print("\nREVERSE DCF — MARKET EXPECTATIONS")
print(f"Reference share price: ${market_price:.2f}")
print(f"Implied enterprise value: ${required_ev:,.2f}M")
print(f"Required 2031 EBIT margin: {required_margin:.1%}")

print("\nLIMITATIONS:")
print("Uses 2025 financial balances with a September 2026 price.")
print("Excludes detailed conversion and dilution adjustments.")
print("This is a diagnostic expectation, not a validated price target.")
