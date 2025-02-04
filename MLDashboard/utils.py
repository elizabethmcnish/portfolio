import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error
import duckdb
import numpy as np
import plotly.express as px

def train_rfr_model(train_X, train_y, max_leaf_node):
    rfr_model = RandomForestRegressor(max_leaf_nodes=max_leaf_node, random_state=1)
    rfr_model.fit(train_X, train_y)

    return rfr_model


def merge_and_clean_data():
    collision_data = pd.read_csv("data/dft-road-casualty-statistics-collision-2023.csv")
    vehicles_data = pd.read_csv("data/dft-road-casualty-statistics-vehicle-2023.csv")
    
    return duckdb.query(
        '''
            SELECT 
                vd.*,
                cd.*
            FROM vehicles_data vd
            LEFT JOIN collision_data cd
                ON vd.accident_reference = cd.accident_reference
        '''
    ).df()
	# df = df[df["generic_make_model"] != "-1"]
	# df["generic_make_model"].describe(include='all')


def make_predictions(model, *kwargs):
    Ynew = model.predict(kwargs)
    st.write("X=%s, Predicted=%s" % (kwargs[0], Ynew[0]))
    # for i in range(len(Xnew)):
    #     st.write("X=%s, Predicted=%s" % (Xnew[i], Ynew[i]))

# Optimising model for max_leaf_node
def get_mae(max_leaf_nodes, train_X, train_y):
    model = RandomForestRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    

def plot_maes(train_X, val_X, train_y, val_y):
    max_leaf_nodes_list = np.arange(10, 201, 10)
    maes = []
    for max_leaf_node in max_leaf_nodes_list:
        mae = get_mae(max_leaf_node, train_X, train_y)
        maes.append(mae)

    df = pd.DataFrame(dict(
        x = max_leaf_nodes_list,
        y = maes
    ))

    return px.line(
        df,
        x = "x", 
        y = "y", 
        markers = True,
        title = "Max Leaf Nodes vs MAE for model validation using Random Forest Regression"
    )

# Dynamically build filters
def build_filters(df, variable_list):
    filters = []
    values = []
    ncol = len(variable_list)
    cols = st.columns(ncol)
    for i, var in enumerate(variable_list):
        with cols[i]: 
            
            value = st.number_input(
                label=f"{var}",
                placeholder=f"Enter a value for {var}",
                min_value=df[var].min(),
                max_value=df[var].max(),
                value=int((df[var].min())+(df[var].max())/2),
                step=1,  
                key=f"{var}_input"
            )
            
            filters.append((var))
            values.append((value))
    
    return filters, values