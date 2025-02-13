import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score, precision_score, recall_score

import utils as ut

print("Installs Complete")

st.set_page_config(
    page_title="ML Dashboard",
    page_icon="💪🏼",
    layout="wide",
    menu_items={"Report a bug": "mailto:mlizzie.mcnish@gmail.com?subject=Bug in ML Dashboard!"},
)

raw_data_link = "https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-accidents-safety-data"

with st.sidebar:
    st.info(
        """
        The following dashboard models the incident severity score of road accidents, 
        based on three continuous input variables (see inputs below). 

        The following model uses Random Tree Regression and Classification methods.

        The model has been trained using historic UK Road Accident data (2023), 
        from the Government Department for Transport. See [:grey[this link]]({raw_data_link}) for the original datasets.

        Categoric mappings:

        | Category    | 1 | 2 | 3 |
        | -------- | ------- | ------- | ------- |
        | Sex  | Male    | Female | Unknown |
    """
    )
    st.warning(
        """
        TODO: Incorporate data from past 5 years, from various data sources.

        TODO: Build out categoric modelling.
    
        TODO: Use Optuna libraries to optimise models further.
    """
    )

st.title("Modelling Accident Severity using UK Road Accidents Data")


# Load, merge, and clean data
data = ut.merge_and_clean_data()

# Create dynamic variable inputs
data_type_input = st.selectbox(
    label="Data Type",
    placeholder="Select either continuous or categoric data",
    options=["Continuous", "Categoric"],
)

if data_type_input == "Continuous":
    variables_list = (data.select_dtypes(include=[np.number])).columns.to_list()
elif data_type_input == "Categoric":
    variables_list = (data.select_dtypes(include=[np.object_])).columns.to_list()
else:
    st.warning("Select a data type")
    st.stop()

if data_type_input == "Continuous":
    variable_list_input = st.multiselect(
        "Select X features", variables_list, default=["sex_of_driver", "age_of_driver", "age_of_vehicle"]
    )
else:
    variable_list_input = st.multiselect(
        "Select X features",
        variables_list,
        default="generic_make_model",
    )

if not variable_list_input:
    st.warning("Enter a combination of input filters")
    st.stop()

filters, values = ut.build_filters(data, variable_list_input)


# Define variables for training model
X = data[variable_list_input]
y = data["accident_severity"]

dcol1, dcol2 = st.columns(2)
dcol3, dcol4 = st.columns(2)

with dcol1.container(border=True):
    st.header("Train")
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

    max_leaf_node_input = st.number_input(
        label="Max Leaf Nodes Input",
        placeholder="Enter integer",
        step=1,
        min_value=2,
        value=5,
    )

    mcol1, mcol2, mcol3 = st.columns(3)
    if data_type_input == "Continuous":
        model = ut.train_rfr_model(train_X, train_y, max_leaf_node=max_leaf_node_input)
        predictions = model.predict(val_X)

        mcol1.metric(
            label=f"Mean Absolute Error (3dp)",
            value=round((mean_absolute_error(val_y, predictions)), 3),
        )

        mcol2.metric(
            label="Root Mean Squared Error (3dp)", value=round(np.sqrt(mean_squared_error(val_y, predictions)), 3)
        )

    elif data_type_input == "Categoric":
        dummy_data = pd.get_dummies(X, dtype=float)
        train_X, val_X, train_y, val_y = train_test_split(dummy_data, y, random_state=0)
        model = ut.train_rfc_model(train_X, train_y, max_leaf_node=max_leaf_node_input)
        predictions = model.predict(val_X)
        mcol1.metric(
            label=f"Accuracy Score (3dp)",
            value=round((accuracy_score(val_y, predictions)), 3),
        )

        # mcol2.metric(label="Precision Score (3dp)", value=round(precision_score(val_y, predictions), 3))

        # mcol3.metric(label="Recall Score (3dp)", value=round(recall_score(val_y, predictions), 3))

if data_type_input == "Categoric":
    st.error("Categoric modelling under construction")
    st.stop()

else:
    with dcol2.container(border=True):
        st.header("Optimise")
        st.info(
            "Use the max leaf node input and plot below to optimise the max leaf nodes for the model. "
            + "Min leaf node = 10."
        )

        max_leaf_node_input = st.number_input(
            label="Max Leaf Node",
            placeholder="Enter integer",
            step=10,
            min_value=20,
            value=50,
        )

        plot_fig_button = st.button(
            label="Run Plot",
        )

        if plot_fig_button:
            ut.plot_maes(train_X, train_y, max_node=max_leaf_node_input)

    with dcol3.container(border=True):
        st.header("Predict")
        run_model_button = st.button(
            label="Run Model",
        )

        if run_model_button:
            on_click = ut.make_predictions(model, values)

    with dcol4.expander(label="See full dataset", expanded=False):
        st.dataframe(data)
