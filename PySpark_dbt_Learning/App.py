import streamlit as st
import pandas as pd

from sql_modelling import clean_data_with_sql


employees_df = pd.read_csv("data/employees.csv")
dates_df = pd.read_csv("data/dates.csv")

# Processing data using SQL
sql_cleaned = clean_data_with_sql()


# Processing data using dbt

st.dataframe(sql_cleaned)
