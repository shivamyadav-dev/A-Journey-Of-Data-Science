
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression



def train_model():
    """
    This function loads the data, cleans it, trains the model, and returns
    the trained model, scaler, and the list of feature columns.
    """
    # --- 1. DATA PREPARATION ---
   
    try:
        data = pd.read_csv(r"C:\Users\Shivam Kumar yadav\OneDrive\Desktop\FSDS\Machine Learning (ML)\class notes\03_Regularization (L1,L2)\car-mpg.csv")
    except FileNotFoundError:
        # If the file is not found, display an error in the app and stop.
        st.error("Error: The CSV file was not found at the specified path. Please update the path in the script.")
        st.stop()

    # Drop the car_name column as it's not needed for prediction
    data = data.drop(['car_name'], axis=1)

    # Handle the 'origin' column with one-hot encoding
    data['origin'] = data['origin'].replace({1: 'america', 2: 'europe', 3: 'asia'})
    data = pd.get_dummies(data, columns=['origin'], prefix='', prefix_sep='')

    # Handle missing values in 'horsepower'
    data['hp'] = data['hp'].replace('?', np.nan)
    data['hp'] = pd.to_numeric(data['hp'])
    data = data.fillna(data.median())

    # --- 2. FEATURE ENGINEERING AND SCALING ---
    # Separate features (X) and target (y)
    X = data.drop('mpg', axis=1)
    y = data['mpg']
    
    # Get the list of columns to ensure the order is consistent
    model_columns = X.columns.tolist()

    # Create and fit the scaler on the entire dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- 3. MODEL TRAINING ---
    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Return the necessary components for prediction
    return model, scaler, model_columns

# --- LOAD THE MODEL (runs only once thanks to caching) ---
model, scaler, model_columns = train_model()


# --- STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="Car MPG Predictor", layout="centered")
st.title('🚗 Car Fuel Efficiency (MPG) Predictor')
st.markdown("This app predicts the **Miles Per Gallon (MPG)** of a car based on its specifications.")
st.divider()

# --- USER INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    cyl = st.number_input('Cylinders', 3, 8, 8, 1)
    disp = st.number_input('Displacement (cu. in.)', 60.0, 500.0, 304.0)
    hp = st.number_input('Horsepower', 40.0, 250.0, 150.0)
    wt = st.number_input('Weight (lbs)', 1500.0, 5500.0, 3449.0)
with col2:
    acc = st.number_input('Acceleration (sec to 60mph)', 8.0, 25.0, 12.0)
    yr = st.slider('Model Year', 70, 82, 70)
    origin = st.selectbox('Origin', ['america', 'europe', 'asia'])

# --- PREDICTION LOGIC ---
if st.button('Predict MPG', type="primary"):
    # Create a DataFrame from the user's input
    input_data = pd.DataFrame([[cyl, disp, hp, wt, acc, yr]], columns=['cyl', 'disp', 'hp', 'wt', 'acc', 'yr'])
    
    # Add the one-hot encoded origin column
    input_data[origin] = 1
    
    # Align the input data columns with the model's training columns
    input_df_aligned = input_data.reindex(columns=model_columns, fill_value=0)
    
    # Scale the input data using the loaded scaler
    input_scaled = scaler.transform(input_df_aligned)
    
    # Make the prediction
    prediction = model.predict(input_scaled)
    predicted_mpg = round(prediction[0], 2)
    
    # Display the result
    st.success(f'**Predicted Fuel Efficiency:**')
    st.markdown(f"<h1 style='text-align: center; color: #2E8B57;'>{predicted_mpg} MPG</h1>", unsafe_allow_html=True)

