
import streamlit as st
from copy import deepcopy
import project1_model as model

st.set_page_config(page_title="MP Materials Workbench", layout="wide")

WACC = 0.11
GROWTH = 0.03

def calculate_ev(rows):
    pv = sum(r["fcff"] / (1 + WACC) ** t
             for t, r in enumerate(rows, 1))
    revenue = rows[-1]["revenue"] * (1 + GROWTH)
    terminal_fcff = revenue * 0.20 * 0.75 * (1 - GROWTH / 0.12)
    terminal_pv = (terminal_fcff / (WACC - GROWTH)) / (1 + WACC) ** 5
    return pv + terminal_pv

def reset():
    st.session_state.margin = 14.1
    st.session_state.capex = 100

st.title("MP Materials — Analyst Workbench")
st.write("FIN 43900 | Five-Year Financial Model | USD Millions")
st.write("Adjust assumptions to see how they affect financial results.")

st.sidebar.header("Operating Assumptions")

margin = st.sidebar.slider(
    "Gross Margin (%)", 12.1, 16.1, 14.1, 0.1, key="margin"
)

capex = st.sidebar.slider(
    "Capital Spending (% of Base)", 90, 110, 100, 5, key="capex"
)

st.sidebar.button("Reset to Base", on_click=reset)
st.sidebar.caption(
    "Bounds come from the Lab 11 sensitivity ranges, "
    "not management guidance."
)

inputs = model.fresh_base_inputs()

for year in model.YEARS:
    inputs["annual"][year]["GROSS_MARGIN"] = margin / 100
    inputs["annual"][year]["CAPEX"] *= capex / 100

rows = model.project(inputs)
base = model.project()

ev = calculate_ev(rows)
base_ev = calculate_ev(base)

st.header("Model Validation")

try:
    model.assert_balanced(rows)
    valid = True
    st.success("PASS — Accounting and liquidity checks")
except ValueError as error:
    valid = False
    st.error(f"FAIL — {error}")

st.header("Financial Results")

a, b, c = st.columns(3)

a.metric("Enterprise Value", f"${ev:,.2f}M",
         f"${ev-base_ev:+,.2f}M vs Base")
b.metric("2030 Operating Income",
         f"${rows[-1]['operating_income']:,.2f}M")
c.metric("2030 FCFF", f"${rows[-1]['fcff']:,.2f}M")

if ev < 0:
    st.warning("Negative modeled EV — not a stock price.")

if not valid:
    st.warning("Scenario is not financially feasible under current constraints.")

st.header("Five-Year Financial Statements")

table = [
    {
        "Year": r["year"],
        "Revenue": round(r["revenue"], 2),
        "Operating Income": round(r["operating_income"], 2),
        "FCFF": round(r["fcff"], 2),
        "Ending Cash": round(r["cash"], 2),
        "Balance Gap": round(r["balance_gap"], 6)
    }
    for r in rows
]

st.dataframe(table, hide_index=True, use_container_width=True)

st.header("Sensitivity Results")
st.write(f"Base Enterprise Value: ${base_ev:,.2f}M")
st.write(f"Selected Enterprise Value: ${ev:,.2f}M")
st.write(f"Change from Base: ${ev-base_ev:+,.2f}M")

st.header("Failure Detection Test")

inject = st.checkbox("Inject $10M accounting error")

if inject:
    test = deepcopy(rows)
    test[0]["balance_gap"] += 10
    try:
        model.assert_balanced(test)
        st.error("ERROR: Corrupted model was not rejected.")
    except ValueError as error:
        st.error(f"EXPECTED FAILURE DETECTED: {error}")
else:
    st.info("No artificial error injected.")

st.caption(
    "Illustrative analysis. The app uses the existing MP pro-forma "
    "and simplified DCF assumptions."
)
