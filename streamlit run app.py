import streamlit as st
import pandas as pd

st.set_page_config(page_title="Compounding Calculator", page_icon="💰")

st.title("💰 Compounding Calculator")
st.write("Compare returns with reinvesting vs withdrawing monthly.")

# Inputs
principal = st.number_input("Initial Amount (₹)", min_value=0.0, value=100000.0, step=100.0)
monthly_rate_percent = st.number_input("Monthly Return (%)", min_value=0.0, value=5.0, step=0.1)
months = st.number_input("Number of Months", min_value=1, value=12, step=1)

monthly_rate = monthly_rate_percent / 100

# --- Reinvesting (compounding) ---
final_reinvest = principal * (1 + monthly_rate) ** months
profit_reinvest = final_reinvest - principal

# --- Monthly Withdrawal (no compounding) ---
monthly_payout = principal * monthly_rate
total_withdrawal = monthly_payout * months
profit_withdrawal = total_withdrawal

# Output
st.subheader("📈 Results")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔁 Reinvesting Every Month")
    st.write(f"**Final Amount:** ₹{final_reinvest:,.2f}")
    st.write(f"**Total Profit:** ₹{profit_reinvest:,.2f}")

with col2:
    st.markdown("### 💵 Withdrawing Monthly")
    st.write(f"**Monthly Withdrawal:** ₹{monthly_payout:,.2f}")
    st.write(f"**Total Withdrawal in {months} months:** ₹{total_withdrawal:,.2f}")
    st.write(f"**Total Profit:** ₹{profit_withdrawal:,.2f}")

# Comparison summary
st.subheader("📊 Comparison Summary")
st.write(f"**Extra earnings due to compounding:** ₹{profit_reinvest - profit_withdrawal:,.2f}")

# Chart Data
df = pd.DataFrame({
    "Month": list(range(1, months + 1)),
    "Reinvested Amount": [principal * (1 + monthly_rate) ** m for m in range(1, months + 1)],
    "Total Withdrawal (No Compounding)": [monthly_payout * m for m in range(1, months + 1)]
})

st.line_chart(df, x="Month", y=["Reinvested Amount", "Total Withdrawal (No Compounding)"])

st.info("This tool is for financial comparison and educational use only.")
