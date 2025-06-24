#import the necessary libraries
import streamlit as st
from utils.data_loader import load_data
import os

#set the page config: title and dark mode layout
st.set_page_config(page_title="Financial Transactions Dashboard", layout="wide", initial_sidebar_state="expanded")

#title and intro text
st.title("Financial Transactions Dashboard - Main Menu")
st.header("Welcome to the dashboard 👋")
st.write(
    """
    This Streamlit application provides an *analytical overview* of international stock transactions
    for the year 2024. \n 
    The system is built on **a star schema model** composed of *fact* and *dimension tables*,
    and supports interactive visual analysis by time and geography. You can explore transaction trends, 
    industries, sectors and symbol-level insights using the pages in the sidebar.
    """
)

#horizontal rule
st.markdown("---")

#dataset download section
labels = {
    "dim_geography.csv": "Geography dimension",
    "dim_symbol.csv": "Symbol dimension",
    "dim_time.csv": "Time dimension",
    "dim_transaction_type.csv": "Transaction Type",
    "fact_transactions.csv": "Fact transactions"
}

st.subheader("Download Dataset Files ⬇️")
st.write("You can download all the datasets I used here:")

data_dir = "data"
csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

for i in range(0, len(csv_files), 3):
    cols = st.columns(3)
    for col, filename in zip(cols, csv_files[i:i+3]):
        label = labels.get(filename, f"Download {filename}")
        with open(os.path.join(data_dir, filename), "rb") as f:
            col.download_button(
                label=label,
                data=f,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )

st.markdown("### Author references 📇")
col1, col2 = st.columns(2)

with col1:
    st.link_button(
        label="LinkedIn",
        url="https://www.linkedin.com/in/valerio-botto-4844b2190/",
        use_container_width=True
    )

with col2:
    st.link_button(
        label="GitHub",
        url="https://github.com/ValerioBotto",
        use_container_width=True
    )

st.write("\n")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("data/logo.png", use_container_width=True)
