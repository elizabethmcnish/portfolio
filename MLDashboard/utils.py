import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error
import duckdb
import numpy as np
import plotly.express as px


def train_rfr_model(train_X, train_y, max_leaf_node):
    model = RandomForestRegressor(max_leaf_nodes=max_leaf_node, random_state=1)
    model.fit(train_X, train_y)

    return model


def train_rfc_model(train_X, train_y, max_leaf_node):
    model = RandomForestClassifier(max_leaf_nodes=max_leaf_node, random_state=1)
    model.fit(train_X, train_y)

    return model


def merge_and_clean_data():
    collision_data = pd.read_csv("data/dft-road-casualty-statistics-collision-2023.csv")
    vehicles_data = pd.read_csv("data/dft-road-casualty-statistics-vehicle-2023.csv")

    return duckdb.query(
        """
            SELECT 
                vd.*,
                cd.*
            FROM vehicles_data vd
            LEFT JOIN collision_data cd
                ON vd.accident_reference = cd.accident_reference
        """
    ).df()


def make_predictions(model, *kwargs):
    Ynew = model.predict(kwargs)
    st.write("X = %s" % (kwargs[0]))
    st.write("Predicted = %s" % (Ynew[0]))


# Optimising model for max_leaf_node
def get_mae(max_leaf_nodes, train_X, train_y):
    model = train_rfr_model(train_X, train_y, max_leaf_nodes)
    predictions = model.predict(train_X)

    return mean_absolute_error(train_y, predictions)


# Plotting maes
def plot_maes(train_X, train_y, max_node):
    max_leaf_nodes_list = np.arange(10, max_node, 10).tolist()
    maes = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    total_steps = len(max_leaf_nodes_list)

    for i, max_leaf_node in enumerate(max_leaf_nodes_list):
        mae = get_mae(max_leaf_node, train_X, train_y)
        maes.append(mae)

        # Update progress bar
        progress = int((i + 1) / total_steps * 100)
        progress_bar.progress(progress)
        status_text.text(f"Processing {i+1}/{total_steps}...")

    progress_bar.empty()
    status_text = st.empty()

    df = pd.DataFrame(dict(x=max_leaf_nodes_list, y=maes))

    maes_fig = px.line(
        df,
        x="x",
        y="y",
        markers=True,
        title="Max Leaf Nodes vs MAE for model validation using Random Forest Regression",
    )

    return st.plotly_chart(maes_fig, use_container_width=True)


# Dynamically build filters
def build_filters(df, variable_list):
    filters = []
    values = []
    ncol = len(variable_list)
    cols = st.columns(ncol)

    value = None

    for i, var in enumerate(variable_list):
        with cols[i]:
            if np.issubdtype(df[var].dtype, np.number):
                value = st.number_input(
                    label=f"{var}",
                    placeholder=f"Enter a value for {var}",
                    min_value=df[var].min(),
                    max_value=df[var].max(),
                    value=int((df[var].min()) + (df[var].max()) / 2),
                    step=1,
                    key=f"{var}_input",
                )

            elif np.issubdtype(df[var].dtype, np.object_):
                value = st.selectbox(
                    label=f"{var}",
                    placeholder=f"Enter a value for {var}",
                    options=df[var].unique(),
                    key=f"{var}_input",
                )

        filters.append((var))
        values.append((value))

    return filters, values
