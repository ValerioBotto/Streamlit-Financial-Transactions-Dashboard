import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    base_path = "data"
    fact = pd.read_csv(os.path.join(base_path, "fact_transactions.csv"))
    dim_time = pd.read_csv(os.path.join(base_path, "dim_time.csv"))
    dim_symbol = pd.read_csv(os.path.join(base_path, "dim_symbol.csv"))
    dim_geo = pd.read_csv(os.path.join(base_path, "dim_geography.csv"))
    dim_tt = pd.read_csv(os.path.join(base_path, "dim_transaction_type.csv"))
    return fact, dim_time, dim_symbol, dim_geo, dim_tt