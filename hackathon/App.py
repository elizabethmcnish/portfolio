import streamlit as st
from google import genai
import pandas as pd
import plotly.graph_objects as go

from google import genai
from google.genai import types

from data_loaders import get_items_from_previous_shop

client = genai.Client(
    vertexai=True,
    project="electricwin25lon-512",
    location="us-central1",
)

model = "gemini-2.0-flash-001"

st.set_page_config(
    page_title="Food Waste Dashboard",
    page_icon="💪🏼",
    layout="wide",
)

st.title("Food Waste Dashboard")


st.header("Predict Waste")


food_data = pd.read_csv("data/dummy_shop_data.csv")
waste_data = pd.read_csv("data/dummy_waste_data.csv")

most_recent_shop_df, previous_shop_dict = get_items_from_previous_shop(food_data)

st.info(f'''
    You bought these item in your most recent shop: 
        
    {most_recent_shop_df["Item_Name"].values}. 

    Below, please input how many items were wasted.
''')
user_inputs = {}

for item in previous_shop_dict:
    user_inputs[item["item_name"]] = st.number_input(
        label=item["item_name"], 
        min_value=0,
        max_value=item["quantity"],
        key=f"{item["item_name"]}_input",
    )


def generate(user_inputs):
    contents = [f"""What is the monetary value and greenhouse gas emissions associated to wasting {value} {key}s from the average UK supermarket?
        Return outputs in the following JSON schema:
        
        {{
        "type": "object",
        "properties": {{
            "item_type": {{
            "type": "string",
            "description": "The type of item being priced (e.g., apples, rice, chicken)."
            }},
            "monetary_value": {{
            "type": "string",
            "pattern": "^£\\d+$",
            "description": "The total price in GBP (£ followed by an integer)."
            }},
            "greenhouse_gas_emissions": {{
            "type": "string",
            "pattern": "^£\\d+$",
            "description": "The total greenhouse gas emissions in kgC02e."
            }}
                
        }},
        "required": ["item_type", "monetary_value", "greenhouse_gas_emissions"]
        }}
        """ for key, value in user_inputs.items()]

    # TODO: handle 0 values
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        st.write(chunk.text, end="")


generate(user_inputs)

with st.expander(label="Expand for full data on food shops"):
    st.dataframe(food_data)

with st.expander(label="Expand for full data on waste"):
    st.dataframe(waste_data)
        

def find_top_waste():
    sorted_waste = waste_data.groupby('Item_Name').sum("Quantity").sort_values('Quantity', ascending=False)
    top3 = sorted_waste.iloc[0:3]
    most_wasted_str = ', '.join(list(top3.index))
    
    return most_wasted_str

most_wasted_str = find_top_waste()
    
st.write(f"Your most wasted items historically are {most_wasted_str}.\n")

def generate_tips(most_wasted_str):

    contents = [f"I tend to waste {most_wasted_str}. How can I reduce my food waste for these items."]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        st.write(chunk.text, end="")
        

def plot_spend_vs_lost(food_data, waste_data):
    food_data = food_data.sort_values('Date')
    food_data['flagged'] = False
    waste_data = waste_data.sort_values('Date')
    # Flag the most recent bought item for each thrown away item
    for index, row in waste_data.iterrows():
        item = row['Item_Name']
        thrown_date = row['Date']
        
        # Find the most recent bought entry before the thrown date
        mask = (food_data['Item_Name'] == item) & (food_data['Date'] <= thrown_date)
        recent_bought_index = food_data[mask].index.max()  # Get the latest bought index
    
        if pd.notna(recent_bought_index):  # If a valid match is found
            food_data.loc[recent_bought_index, 'flagged'] = True
   # Group by date and calculate total spend for all items and unflagged items
    total_spend = food_data.groupby('Date')['Price'].sum().reset_index()
    total_spend.columns = ['Date', 'Total_Spend']
    
    unflagged_spend = food_data[~food_data['flagged']].groupby('Date')['Price'].sum().reset_index()
    unflagged_spend.columns = ['Date', 'Unflagged_Spend']
    
    # Merge the two dataframes
    merged_data = pd.merge(total_spend, unflagged_spend, on='Date', how='left')
    merged_data['Unflagged_Spend'] = merged_data['Unflagged_Spend'].fillna(0)
    
    # Create the grouped bar chart
    # Create the grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=merged_data['Date'],
        y=merged_data['Total_Spend'],
        name='Cost of shop',
        marker_color='rgb(55, 83, 109)',
        text=[f"£{val:.2f}" for val in merged_data['Total_Spend']],
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    fig.add_trace(go.Bar(
        x=merged_data['Date'],
        y=merged_data['Unflagged_Spend'],
        name='Cost of shop without wasted items',
        marker_color='rgb(26, 118, 255)',
        text=[f"£{val:.2f}" for val in merged_data['Unflagged_Spend']],
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    # Update the layout with explicit x-axis ticks
    fig.update_layout(
        title='Total Spend by Date',
        xaxis_title='Date',
        yaxis_title='Total Spend (£)',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        plot_bgcolor='white',
        margin=dict(t=50, b=50, l=50, r=50),
        yaxis=dict(range=[0, max(merged_data['Total_Spend']) * 1.2])
    )
    
    # Force display of all x-axis tick labels
    fig.update_xaxes(
        tickmode='array',
        tickvals=merged_data['Date'].tolist(),  # Explicitly set tick positions
        ticktext=merged_data['Date'].tolist(),  # Explicitly set tick labels
        tickangle=-45 if len(merged_data) > 5 else 0  # Angle labels if many dates
    )
    
    # Add gridlines
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    )
    
    return fig
        
   
    
# Format for Streamlit app
st.title('Food Spending Analysis')
st.write('The plot below shows how much cheaper your previous shops would be if you didnt buy items that you do not use')
st.plotly_chart(plot_spend_vs_lost(food_data, waste_data), use_container_width=True)

