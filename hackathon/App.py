import streamlit as st
from google import genai
import pandas as pd

from google import genai
from google.genai import types

st.set_page_config(
    page_title="Food Waste Dashboard",
    page_icon="💪🏼",
    layout="wide",
)

st.title("Food Waste Dashboard")

food_data = pd.read_csv("data/dummy_shop_data.csv")
waste_data = pd.read_csv("data/dummy_waste_data.csv")

# TODO: add prediction

col1, col2 = st.columns(2)

number_input = col1.number_input(label="Weight of items wasted (kg)", min_value=0, value=5, step=1)
item_type_input = col2.text_input(label="No. of items wasted", value="Oranges")


def generate(no_items: int, item_type: str):
    client = genai.Client(
        vertexai=True,
        project="electricwin25lon-512",
        location="us-central1",
    )

    model = "gemini-2.0-flash-001"
    contents = [f"What is the monetary value of {no_items}kg of {item_type} from the average UK supermarket"]
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


generate(no_items=number_input, item_type=item_type_input)

