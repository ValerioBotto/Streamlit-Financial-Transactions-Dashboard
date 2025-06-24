# pages/2_CountryAnalysis.py

import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.line_chart import plot_country_transactions
from utils.bar_plot import plot_top_industries_by_type


st.set_page_config(page_title="Country Analysis Dashboard", layout="wide")

#load data
fact, dim_time, dim_symbol, dim_geo, dim_tt = load_data()

#merge fact + time + symbol + geography (correct join: geography_id with country_id)
merged = fact \
    .merge(dim_time, on="date_id", how="left") \
    .merge(dim_symbol, on="symbol_id", how="left") \
    .merge(dim_geo, left_on="geography_id", right_on="country_id", how="left")

#rename for clarity
country_list = merged.loc[:, "country"].dropna().unique()

#ensure Date column is datetime only
merged["Date"] = pd.to_datetime(merged["Date"])

#--------------------------------------------
#sidebar - country selector
#--------------------------------------------
st.sidebar.header("Country Filter")

#unique country list
country_list = merged["country"].dropna().unique()

#show "United States of America" by default
selected_country = st.sidebar.selectbox(
    "Select a country:",
    options=sorted(country_list),
    index=list(sorted(country_list)).index("United States of America") if "United States of America" in country_list else 0
)

#filter by selected country
filtered = merged[merged["country"] == selected_country].copy()

#--------------------------------------------
#main layout - line chart
#--------------------------------------------
st.title("Country Analysis")
st.subheader(f"Total Transactions in {selected_country} - 2024")

fig = plot_country_transactions(filtered)
st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------
#metrics for selected country
#--------------------------------------------
st.subheader(f"Summary Metrics for {selected_country}")

total_buy = filtered[filtered["transaction_type_id"] == 1].shape[0]
total_sell = filtered[filtered["transaction_type_id"] == 2].shape[0]

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total BUY Transactions", value=total_buy)
with col2:
    st.metric(label="Total SELL Transactions", value=total_sell)

#--------------------------------------------
#bar charts for the top industries according to transaction type
#--------------------------------------------

st.markdown("---")


from utils.bar_plot import plot_top_industries_by_type


col1, col2 = st.columns(2)

with col1:
    fig_buy = plot_top_industries_by_type(filtered, "BUY")
    if fig_buy:
        st.plotly_chart(fig_buy, use_container_width=True)

with col2:
    fig_sell = plot_top_industries_by_type(filtered, "SELL")
    if fig_sell:
        st.plotly_chart(fig_sell, use_container_width=True)


top_symbol = (
    filtered.groupby("symbol")["transaction_type_id"]
    .count()
    .sort_values(ascending=False)
    .idxmax()
)
st.subheader(f"The Most Traded Symbol for {selected_country} in 2024 is: **{top_symbol}**")
