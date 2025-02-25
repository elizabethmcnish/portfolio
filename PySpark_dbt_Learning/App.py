import streamlit as st
import pandas as pd

from data_loaders import clean_data_with_sql, load_data_from_duckdb

st.set_page_config(page_title="Data Modelling: SQL vs dbt", layout="wide", page_icon="🦋")

dbt_col, sql_col = st.columns(2)

with dbt_col.container(border=True):
    st.subheader("Modelling Data with dbt")

    # Processing data using dbt models (pre-loaded)
    dbt_table, dbt_ttl = load_data_from_duckdb()

    st.dataframe(dbt_table, use_container_width=True)
    st.write(f"Time to load: {dbt_ttl} s")

with sql_col.container(border=True):
    st.subheader("Modelling Data with SQL and CTEs")

    employees_df = pd.read_csv("data/employees.csv")
    dates_df = pd.read_csv("data/dates.csv")

    # Processing data using SQL
    sql_cleaned, sql_ttl = clean_data_with_sql(dates_df=dates_df, employees_df=employees_df)
    st.dataframe(sql_cleaned, use_container_width=True)
    st.write(f"Time to load: {sql_ttl} s")
