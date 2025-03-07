
import pandas as pd 
import streamlit as st

def get_items_from_previous_shop(data):
    most_recent_shop = data[data['Date'] == data['Date'].max()]
    
    # Group by 'Item_Name' and sum 'Quantity'
    most_recent_shop = most_recent_shop.groupby('Item_Name', as_index=False)['Quantity'].sum()
    
    # Create list of dictionaries
    most_recent_shop_dict = []
    for _, row in most_recent_shop.iterrows():  # Corrected iteration
        most_recent_shop_dict.append({
            "item_name": row["Item_Name"],  # Directly access value
            "quantity": row["Quantity"]
        })

    return most_recent_shop, most_recent_shop_dict