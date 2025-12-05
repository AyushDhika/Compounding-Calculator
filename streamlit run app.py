import streamlit as st

st.set_page_config(page_title="Compounding Calculator", page_icon="💰")

st.title("💰 Compounding Calculator")
st.write("Calculate how your investment grows if monthly returns are reinvested.")

# Input fields
principal = st.number_input("Initial Amount (₹)", min_value=0.0, value=10000.0, step=100.0)
monthly_rate_percent = st.number_input("Monthly Return (%)", min_value=0.0, value=5.0, step=0.1)
months = st.number_input("Number of Months", min_value=1, value=12, step=1)

# Convert % to decimal
monthly_rate = monthly_rate_percent / 100

# Calculate final amount
final_amount = principal * (1 + monthly_rate) ** months
profit = final_amount - principal

st.subheader("📈 Results")
st.write(f"**Final Amount:** ₹{final_amount:,.2f}")
st.write(f"**Total Profit:** ₹{profit:,.2f}")

# Graph
import pandas as pd

data = {
    "Month": list(range(1, months + 1)),
    "Amount": [principal * (1 + monthly_rate) ** m for m in range(1, months + 1)]
}

df = pd.DataFrame(data)
st.line_chart(df, x="Month", y="Amount")

st.info("This calculator is for educational and financial planning purposes only.")
