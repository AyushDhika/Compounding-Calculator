import streamlit as st
import pandas as pd

st.set_page_config(page_title="Investment Plans Dashboard", page_icon="💰", layout="wide")

st.title("💰 Investment Plans Dashboard")
st.write("Compare multiple investment strategies side-by-side.")

# ---------------- INPUTS ----------------
st.sidebar.header("Input Parameters")

principal = st.sidebar.number_input("Initial Amount (₹)", min_value=0.0, value=100000.0, step=1000.0)
months = st.sidebar.number_input("Investment Duration (Months)", min_value=1, value=12, step=1)

st.sidebar.markdown("### Monthly Return Rates (%)")
rate_A = st.sidebar.number_input("Plan A – Monthly Payout (%)", min_value=0.0, value=5.0)
rate_B = st.sidebar.number_input("Plan B – Reinvest Monthly (%)", min_value=0.0, value=5.0)
rate_C = st.sidebar.number_input("Plan C – High Growth Locked (%)", min_value=0.0, value=4.0)
rate_D = st.sidebar.number_input("Plan D – Hybrid Plan (%)", min_value=0.0, value=5.0)

# Convert to decimal
rA, rB, rC, rD = rate_A/100, rate_B/100, rate_C/100, rate_D/100

# ---------------- CALCULATIONS ----------------

# Plan A – Monthly Payout
monthly_payout_A = principal * rA
final_A = principal  # principal remains same
profit_A = monthly_payout_A * months

# Plan B – Monthly Reinvesting (Compounding)
final_B = principal * (1 + rB) ** months
profit_B = final_B - principal

# Plan C – Locked Growth for full duration
final_C = principal * (1 + rC) ** months
profit_C = final_C - principal

# Plan D – Hybrid 50% payout, 50% reinvest
# ---------------- HYBRID PLAN SETTINGS ----------------
st.sidebar.markdown("### Hybrid Plan Settings")
hybrid_reinvest_percent = st.sidebar.slider("Reinvest %", 0, 100, 50)
hybrid_withdraw_percent = 100 - hybrid_reinvest_percent

# Convert to decimals
hybrid_reinvest_ratio = hybrid_reinvest_percent / 100
hybrid_withdraw_ratio = hybrid_withdraw_percent / 100

# ---------------- PLAN D CALCULATION ----------------
# Split principal based on chosen ratio
principal_reinvest = principal * hybrid_reinvest_ratio
principal_withdraw = principal * hybrid_withdraw_ratio

# Reinvested portion (compounds)
reinvest_growth_D = principal_reinvest * (1 + rD) ** months

# Withdrawn portion (fixed monthly payouts)
withdrawal_monthly_D = principal_withdraw * rD
total_withdrawal_D = withdrawal_monthly_D * months

final_D = reinvest_growth_D + principal_withdraw
profit_D = (reinvest_growth_D - principal_reinvest) + total_withdrawal_D
# ---------------- SUMMARY TABLE ----------------

summary = pd.DataFrame({
    "Plan": ["Plan A – Monthly Payout", "Plan B – Full Reinvest", "Plan C – High Growth", "Plan D – Hybrid 50/50"],
    "Final Amount (₹)": [final_A + profit_A, final_B, final_C, final_D],
    "Total Profit (₹)": [profit_A, profit_B, profit_C, profit_D],
})

# ---------------- DISPLAY ----------------
st.header("📊 Plan Comparison Summary")
st.dataframe(summary.style.format({"Final Amount (₹)": "{:,.2f}", "Total Profit (₹)": "{:,.2f}"}))

# ---------------- CHART ----------------
st.header("📈 Profit Comparison Chart")
chart_df = summary.set_index("Plan")["Total Profit (₹)"]
st.bar_chart(chart_df)

# ---------------- GROWTH CHARTS ----------------
st.header("📉 Monthly Growth – Reinvesting Plans Only")

growth_df = pd.DataFrame({
    "Month": list(range(1, months + 1)),
    "Plan B – Reinvest": [principal * (1 + rB) ** m for m in range(1, months + 1)],
    "Plan C – High Growth": [principal * (1 + rC) ** m for m in range(1, months + 1)],
    "Plan D – Reinvest Portion": [(principal/2) * (1 + rD) ** m for m in range(1, months + 1)]
})

st.line_chart(growth_df, x="Month", y=["Plan B – Reinvest", "Plan C – High Growth", "Plan D – Reinvest Portion"])

st.success("Dashboard Ready ✔ – You can customize plan names, rates, and logic anytime.")
