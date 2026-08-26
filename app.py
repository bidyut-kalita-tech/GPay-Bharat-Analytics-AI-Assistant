import streamlit as st
import pandas as pd

st.set_page_config(page_title="Google Pay AI Assistant", page_icon="💳", layout="wide")
st.title("Google Pay (GPay) - AI Insights Assistant")
st.markdown("Query transactional performance, demographics, and risk metrics directly from the UPI dataset.")

@st.cache_data
def load_data():
    df = pd.read_csv("upi_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

try:
    df = load_data()
    total_txns = len(df)
    total_volume = df['amount (INR)'].sum()
    avg_ticket = df['amount (INR)'].mean()
    success_rate = (df['transaction_status'] == 'SUCCESS').mean() * 100
    top_merchant = df.groupby('merchant_category')['amount (INR)'].sum().idxmax()
    top_age_group = df['sender_age_group'].value_counts().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", f"{total_txns:,}")
    col2.metric("Total Volume", f"₹{total_volume:,.2f}")
    col3.metric("Avg Ticket Size", f"₹{avg_ticket:,.2f}")
    col4.metric("Success Rate", f"{success_rate:.2f}%")

    st.divider()

    query = st.text_input("Ask a business question:").lower()

    if query:
        if "volume" in query or "total amount" in query or "revenue" in query:
            st.success(f"📊 Total Volume Processed: ₹{total_volume:,.2f} across {total_txns:,} transactions.")
        elif "success" in query or "failure" in query or "rate" in query:
            failed_count = (df['transaction_status'] == 'FAILED').sum()
            st.success(f"✅ Success Rate: {success_rate:.2f}% | Failed Transactions: {failed_count:,}")
        elif "average" in query or "ticket" in query:
            st.success(f"💳 Average Ticket Size: ₹{avg_ticket:,.2f}")
        elif "merchant" in query or "category" in query:
            cat_spend = df.groupby('merchant_category')['amount (INR)'].sum().sort_values(ascending=False).head(3)
            st.info(f"🛍️ Top Merchant Category: {top_merchant}. Top 3: {', '.join(cat_spend.index.tolist())}.")
        elif "age" in query or "demographic" in query:
            st.success(f"👥 Dominant User Segment: {top_age_group}")
        elif "weekend" in query or "weekday" in query:
            weekend_vol = df[df['is_weekend'] == 1]['amount (INR)'].sum()
            weekday_vol = df[df['is_weekend'] == 0]['amount (INR)'].sum()
            st.info(f"📅 Weekday Volume: ₹{weekday_vol:,.2f} | Weekend Volume: ₹{weekend_vol:,.2f}")
        elif "fraud" in query or "risk" in query:
            fraud_count = df['fraud_flag'].sum()
            st.warning(f"⚠️ Flagged Fraudulent Transactions: {fraud_count:,} ({(fraud_count/total_txns)*100:.3f}%)")
        else:
            st.warning("🤖 Query not recognized. Try asking: 'total volume', 'success rate', 'top merchant', etc.")

except FileNotFoundError:
    st.error("❌ 'upi_data.csv' not found. Ensure upi_data.csv is inside this folder.")