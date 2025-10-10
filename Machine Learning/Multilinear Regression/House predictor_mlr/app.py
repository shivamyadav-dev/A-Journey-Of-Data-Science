import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# --- Page Configuration ---
st.set_page_config(
    page_title="Seattle House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# --- Caching Functions for Performance ---
@st.cache_data
def load_data(path):
    """Loads the dataset from a CSV file."""
    df = pd.read_csv(path)
    return df

@st.cache_resource
def train_model(df):
    """Preprocesses data with selected features and trains the model."""
    df_cleaned = df.drop(['id', 'date'], axis=1)
    feature_cols = [
        'sqft_living', 'grade', 'bedrooms', 'bathrooms',
        'waterfront', 'yr_built', 'lat', 'long'
    ]
    df_model = df_cleaned[feature_cols + ['price']]
    X = df_model.drop('price', axis=1)
    y = df_model['price']
    model = LinearRegression()
    model.fit(X, y)
    return model, X.columns

# --- Main Application ---
try:
    data = load_data("House_data.csv")
    model, feature_names = train_model(data)

    # --- UI Layout ---
    st.title("🏠 Simple House Price Predictor")
    st.markdown("Enter the key details of a house to get an estimated price.")

    # --- User Inputs in Main Area using Columns ---
    st.subheader("Enter House Features")
    
    col1, col2 = st.columns(2)

    with col1:
        sqft_living = st.number_input("Square Feet (Living)", 500, 15000, 1800)
        grade = st.slider("Grade (1-13, higher is better)", 1, 13, 7)
        bedrooms = st.slider("Bedrooms", 1, 10, 3)
        bathrooms = st.slider("Bathrooms", 1.0, 8.0, 2.0, 0.25)
        
    with col2:
        waterfront = st.selectbox("Waterfront View", [0, 1], help="0 = No, 1 = Yes")
        yr_built = st.slider("Year Built", 1900, 2024, 1980)
        lat = st.number_input("Latitude", 47.1, 47.8, 47.5, 0.0001, format="%.4f")
        long = st.number_input("Longitude", -122.5, -121.3, -122.3, 0.0001, format="%.4f")

    # Create a dictionary from the inputs
    user_inputs = {
        'sqft_living': sqft_living,
        'grade': grade,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'waterfront': waterfront,
        'yr_built': yr_built,
        'lat': lat,
        'long': long
    }
    
    # Create a DataFrame from user inputs in the correct order
    input_df = pd.DataFrame([user_inputs], columns=feature_names)

    # --- Prediction Button and Display ---
    if st.button("Predict House Price", type="primary", use_container_width=True):
        input_array = input_df.values
        prediction = model.predict(input_array)
        predicted_price = int(prediction[0])

        st.metric(
            label="Predicted House Price",
            value=f"${predicted_price:,}",
            help="The estimated market value based on the provided features."
        )

except FileNotFoundError:
    st.error("Error: 'House_data.csv' not found. Please make sure the data file is in the same directory as this script.")
except Exception as e:
    st.error(f"An error occurred: {e}")

