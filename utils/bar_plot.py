import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

#barplot for top 3 traded symbols with buy/sell breakdown
def plot_top_symbols(df):
    #compute total transaction count per symbol
    total_counts = (
        df.groupby("symbol_id").size().reset_index(name="Total")
    )

    #compute buy and sell counts
    buy_counts = df[df["transaction_type_id"] == 1].groupby("symbol_id").size().reset_index(name="BUY")
    sell_counts = df[df["transaction_type_id"] == 2].groupby("symbol_id").size().reset_index(name="SELL")

    #merge all counts together
    symbol_counts = total_counts.merge(buy_counts, on="symbol_id", how="left")
    symbol_counts = symbol_counts.merge(sell_counts, on="symbol_id", how="left")

    #replace NaNs with 0
    symbol_counts.fillna(0, inplace=True)

    #keep top 3 symbols by total
    top3 = symbol_counts.sort_values(by="Total", ascending=False).head(3)

    #merge with symbol name
    if "symbol" in df.columns:
        top3 = top3.merge(df[["symbol_id", "symbol"]].drop_duplicates(), on="symbol_id", how="left")
    else:
        top3["symbol"] = top3["symbol_id"].astype(str)

    #create grouped barplot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top3["symbol"], y=top3["Total"], name="Total", marker_color="blue"))
    fig.add_trace(go.Bar(x=top3["symbol"], y=top3["BUY"], name="BUY", marker_color="green"))
    fig.add_trace(go.Bar(x=top3["symbol"], y=top3["SELL"], name="SELL", marker_color="red"))

    fig.update_layout(
        barmode='group',
        xaxis_title="Symbol",
        yaxis_title="Transaction Count",
        showlegend=True,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return fig

#---------------------------------------------------
#barplot for top5 sectors by transaction count
def plot_top_sectors(df):
    #compute top 5 sectors by count
    sector_counts = (
        df.groupby("sector")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .head(5)
    )

    #assign color: highlight top sector in blue, others in grey
    top_sector = sector_counts.iloc[0]["sector"]
    sector_counts["color"] = sector_counts["sector"].apply(
        lambda x: "lightskyblue" if x == top_sector else "lightgrey"
    )

    #create bar chart with custom colors
    fig = px.bar(
        sector_counts,
        x="sector",
        y="count",
        color="color",
        color_discrete_map="identity"
    )

    #remove legend and adjust layout
    fig.update_layout(showlegend=True, margin=dict(t=40, b=20))
    return fig

#---------------------------------------------------
#barplot for top 5 industries

def plot_top_industries(df):
    industry_counts = (
        df.groupby("industry")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .head(5)
    )
    
    #highlight the top industry
    top_industry = industry_counts.iloc[0]["industry"]
    industry_counts["color"] = industry_counts["industry"].apply(
        lambda x: "lightskyblue" if x == top_industry else "lightgray"
    )

    fig = px.bar(
        industry_counts,
        x="industry",
        y="count",
        color="color",
        color_discrete_map="identity"
    )

    fig.update_layout(showlegend=False)

    return fig, top_industry, int(industry_counts.iloc[0]["count"])

#---------------------------------------------------
#barplots for top industries by BUY and SELL transactions
def plot_top_industries_by_type(df: pd.DataFrame, transaction_type: str):
    df = df[df["transaction_type_id"] == (1 if transaction_type == "BUY" else 2)]

    if "industry" not in df.columns:
        return None

    top_industries = (
        df.groupby("industry")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .head(5)
    )

    #setting green for the buy transactions and red for the sell transactions
    highlight_color = "#00FF00" if transaction_type == "BUY" else "#FF0000"
    default_color = "lightgray"
    top_industries["color"] = [highlight_color if i == 0 else default_color for i in range(len(top_industries))]

    fig = px.bar(
        top_industries,
        x="industry",
        y="count",
        title=f"Top 5 Industries by {transaction_type} Transactions",
        color="color",
        color_discrete_map="identity"
    )

    fig.update_layout(showlegend=False)
    return fig