import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import utils as ut

print('Installs Complete')

st.set_page_config(
    page_title="ML Dashboard",
    page_icon="💪🏼",
    layout="wide",
    menu_items={"Report a bug": "mailto:mlizzie.mcnish@gmail.com?subject=Bug in ML Dashboard!"},
)

link = 'https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-accidents-safety-data'

st.title("Modelling UK Road Accidents Data")
st.info(
    '''
        The following dashboard models the incident severity score of road accidents, 
        based on three continuous input variables (see inputs below). 

        The following model uses Random Tree Regression methods.

        The model has been trained using historic UK Road Accident data (2023), 
        from the Government Department for Transport. See [:grey[this link]]({link}) for the original datasets.

        Categoric mappings:

        | Category    | 1 | 2 | 3 |
        | -------- | ------- | ------- | ------- |
        | Sex  | Male    | Female | Unknown |
    '''
)

# Load, merge, and clean data
data = ut.merge_and_clean_data()

# Create dynamic variable inputs
continous_variables_list = (data.select_dtypes(include=[np.number])).columns.to_list()

variable_list = st.multiselect("Select X variables",  
                               continous_variables_list, 
                               default=["sex_of_driver", "age_of_driver", "age_of_vehicle"],
                               )

if variable_list == "":
    st.warning("Enter a combination of input filters")
    st.stop()

filters, values = ut.build_filters(data, variable_list)

# Define variables for training model
X = data[variable_list]
y = data['accident_severity']

dcol1, dcol2 = st.columns(2)

with dcol1.container(border=True):
    st.header("Train and Optimise")
    max_leaf_node_input = st.number_input(
        label = "Max Leaf Nodes Input",
        placeholder = "Enter integer",
        step=1,
        min_value=0,
    )
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)
    rfr_model = ut.train_rfr_model(train_X, train_y, max_leaf_node=max_leaf_node_input)
    predictions = rfr_model.predict(val_X)
    
    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric(
        label=f"Mean Absolute Error at {max_leaf_node_input} leaf nodes",
        value=(mean_absolute_error(val_y, predictions)),
        )

    st.info('Use the plot below to optimise the max leaf nodes for the model')
    maes_fig = ut.plot_maes(train_X, val_X, train_y, val_y)
    st.plotly_chart(maes_fig, use_container_width=True)

with dcol2.container(border=True):
    st.header("Predict")
    st.button(
        label="Run Model",
        on_click=ut.make_predictions(rfr_model, values),
    )

with st.expander(
    label="Full dataset",
    expanded=False,
    ):
    st.dataframe(data)


