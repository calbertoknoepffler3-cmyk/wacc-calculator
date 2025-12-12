
import streamlit as st
import yfinance as yf

st.title("📊 WACC Calculator")

# User Inputs
ticker_input = st.text_input("Enter Ticker Symbol (e.g., AAPL)", value="AAPL")
risk_free_rate = st.number_input("Risk-Free Rate (%)", value=4.0, step=0.1)
market_return = st.number_input("Expected Market Return (%)", value=10.0, step=0.1)
cost_of_debt = st.number_input("Cost of Debt (%)", value=5.0, step=0.1)
tax_rate = st.number_input("Corporate Tax Rate (%)", value=21.0, step=0.1)

if ticker_input:
    ticker = yf.Ticker(ticker_input)

    try:
        info = ticker.info
        market_cap = info.get("marketCap", None)
        total_debt = info.get("totalDebt", None)
        beta = info.get("beta", None)

        if market_cap and total_debt and beta is not None:
            # Convert percentage inputs to decimal
            rf = risk_free_rate / 100
            rm = market_return / 100
            rd = cost_of_debt / 100
            tax = tax_rate / 100

            # Cost of Equity using CAPM
            re = rf + beta * (rm - rf)

            # Capital structure
            E = market_cap
            D = total_debt
            V = E + D

            wacc = (E/V)*re + (D/V)*rd*(1 - tax)

            # Display Results
            st.subheader(f"WACC for {ticker_input.upper()}")
            st.write(f"📈 Beta: {beta:.2f}")
            st.write(f"💰 Market Cap (Equity): ${E:,.0f}")
            st.write(f"🏦 Total Debt: ${D:,.0f}")
            st.write(f"⚖️ Cost of Equity (CAPM): {re*100:.2f}%")
            st.write(f"📉 Cost of Debt: {rd*100:.2f}%")
            st.write(f"🧾 Tax Rate: {tax*100:.2f}%")
            st.success(f"✅ **WACC: {wacc*100:.2f}%**")

        else:
            st.warning("⚠️ Unable to retrieve necessary data (Market Cap, Debt, or Beta). Try a different ticker.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
