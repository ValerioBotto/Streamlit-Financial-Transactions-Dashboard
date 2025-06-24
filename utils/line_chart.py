import pandas as pd
import streamlit as st
import plotly.express as px

def plot_transactions_line_chart(transactions_df: pd.DataFrame):
    #converts the Date column to datetime
    transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])

    #filter only BUY (1) and SELL (2)
    transactions_df = transactions_df[transactions_df['transaction_type_id'].isin([1, 2])]

    #group by day and transaction type
    daily_counts = (
        transactions_df
        .groupby([pd.Grouper(key='Date', freq='D'), 'transaction_type_id'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    #convert numeric columns to strings
    daily_counts.columns = daily_counts.columns.astype(str)

    #rename columns "1" and "2" to "buy" and "sell"
    daily_counts = daily_counts.rename(columns={'1': 'BUY', '2': 'SELL'})
    transaction_columns = ['BUY', 'SELL']
    colors = ['#00FF00', '#FF0000']

    st.line_chart(
        daily_counts,
        x='Date',
        y=transaction_columns,
        color=colors
    )

#----------LINE CHART FOR THE SECOND PAGE-----------

#plot line chart for a selected country (BUY + SELL transactions over time)
def plot_country_transactions(transactions_df: pd.DataFrame):

    #make sure date is in datetime format
    transactions_df["Date"] = pd.to_datetime(transactions_df["Date"])

    #filter only BUY and SELL transactions
    transactions_df = transactions_df[transactions_df["transaction_type_id"].isin([1, 2])].copy()

    #map transaction_type_id to labels
    type_map = {1: "BUY", 2: "SELL"}
    transactions_df["Type"] = transactions_df["transaction_type_id"].map(type_map)

    #remove duplicates (just in case)
    transactions_df = transactions_df.drop_duplicates()

    #round dates to the beginning of the week (Monday)
    transactions_df["Week"] = transactions_df["Date"].dt.to_period("W").apply(lambda r: r.start_time)

    #group by Week and Type to count transactions
    weekly = (
        transactions_df
        .groupby(["Week", "Type"])
        .size()
        .reset_index(name="TransactionCount")
    )

    #generate line chart
    fig = px.line(
        weekly,
        x="Week",
        y="TransactionCount",
        color="Type",
        color_discrete_map={"BUY": "#00FF00", "SELL": "#FF0000"}
    )

    return fig


