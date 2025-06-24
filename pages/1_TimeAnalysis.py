import streamlit as st
import pandas as pd
from datetime import date
from utils.data_loader import load_data
from utils.line_chart import plot_transactions_line_chart
from utils.bar_plot import plot_top_symbols, plot_top_sectors, plot_top_industries

st.title("Time Analysis")

st.caption("Please select the desired time range")

#date filter
start_date = st.date_input(
    "Start date",
    value=date(2024, 1, 1)
)
end_date = st.date_input(
    "End date",
    value=date(2024, 12, 31)
)

#loading the necessary data
fact, dim_time, dim_symbol, dim_geo, dim_tt = load_data()

#joining fact and time dimension
df = fact.merge(dim_time, on='date_id', how='left')

#filtering using the date column
df_filtered = df[
    (pd.to_datetime(df['Date']) >= pd.Timestamp(start_date)) &
    (pd.to_datetime(df['Date']) <= pd.Timestamp(end_date))
]

st.header("Total number of transactions (BUY + SELL)")

plot_transactions_line_chart(df_filtered)

#adding extra information to improve reading
total_buy = df_filtered[df_filtered['transaction_type_id'] == dim_tt[dim_tt['TransactionType'] == 'BUY']['transaction_type_id'].values[0]].shape[0]
total_sell = df_filtered[df_filtered['transaction_type_id'] == dim_tt[dim_tt['TransactionType'] == 'SELL']['transaction_type_id'].values[0]].shape[0]

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total BUY Transactions", value=total_buy)
with col2:
    st.metric(label="Total SELL Transactions", value=total_sell)

st.subheader("Top 3 Traded Symbols by Transaction Type")
fig_symbols = plot_top_symbols(df_filtered.merge(dim_symbol, on="symbol_id"))
st.plotly_chart(fig_symbols, use_container_width=True)


#--------------------------------------------
#top 5 sectors bar chart
#--------------------------------------------
st.subheader("Top 5 Sectors by Transaction Count")
st.caption("This bar chart shows the top 5 sectors with the most amount of transactions (sum of BUY + SELL)")
fig_sectors = plot_top_sectors(df_filtered.merge(dim_symbol, on="symbol_id"))
st.plotly_chart(fig_sectors, use_container_width=True)

filtered_with_sector = df_filtered.merge(dim_symbol[["symbol_id", "sector"]], on="symbol_id", how="left")


#addi textual info below the chart
top_sector = (
    filtered_with_sector.groupby("sector")
    .size()
    .reset_index(name="count")
    .sort_values(by="count", ascending=False)
    .iloc[0]
)

st.write(f"**The sector with the most amount of transactions is \
            `{top_sector['sector']}` with a total of \
                `{top_sector['count']}` transactions.**")



#--------------------------------------------
#top 5 industries bar chart
#--------------------------------------------
st.subheader("Top 5 Industries by Transaction Count")
st.caption("This bar chart shows the top 5 Industries with the most amount of transactions (sum of BUY + SELL)")

df_ind = df_filtered.merge(dim_symbol[["symbol_id", "industry"]], on="symbol_id", how="left")

fig_industries, top_industry, top_count = plot_top_industries(df_ind)
st.plotly_chart(fig_industries, use_container_width=True)
st.markdown(f"**The industry with the most amount of transactions is `{top_industry}` with a total of `{top_count}` transactions.**")