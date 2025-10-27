import streamlit as st
import pickle
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# --- LOAD MODEL AND SCALER ---
# Use st.cache_resource to load these only once
@st.cache_resource
def load_model():
    """Loads the pickled RandomForestRegressor model."""
    try:
        with open('random_forest_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file 'random_forest_model.pkl' not found.")
        st.info("Please run your 'bitcoinmodel.ipynb' notebook to generate the 'random_forest_model.pkl' file and place it in the same directory as this app.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_resource
def load_scaler():
    """Loads the pickled MinMaxScaler."""
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        return scaler
    except FileNotFoundError:
        st.error("Scaler file 'scaler.pkl' not found.")
        st.info("Please run your 'bitcoinmodel.ipynb' notebook to generate the 'scaler.pkl' file and place it in the same directory as this app.")
        return None
    except Exception as e:
        st.error(f"Error loading scaler: {e}")
        return None

# Load the model and scaler
model = load_model()
scaler = load_scaler()

# --- STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="BTC Price Predictor", layout="wide")
st.title("📈 Bitcoin Next-Day Price Predictor")
st.write("Using a Random Forest model trained on 5 years of crypto data.")

# Only proceed if both model and scaler are loaded successfully
if model and scaler:
    
    st.header("Enter Today's Market Data")
    st.info("Provide today's closing prices (in USD) for the following cryptocurrencies. These are the 4 features the model was trained on.")

    # Create columns for a cleaner layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ethereum (ETH)")
        eth_close = st.number_input("ETH Close Price", min_value=0.0, value=3000.0, step=50.0, format="%.2f")
        
        st.subheader("Binance Coin (BNB)")
        bnb_close = st.number_input("BNB Close Price", min_value=0.0, value=500.0, step=10.0, format="%.2f")

    with col2:
        st.subheader("Solana (SOL)")
        sol_close = st.number_input("SOL Close Price", min_value=0.0, value=150.0, step=10.0, format="%.2f")

        st.subheader("Cardano (ADA)")
        ada_close = st.number_input("ADA Close Price", min_value=0.0, value=0.45, step=0.01, format="%.2f")

    st.divider()

    # Prediction Button
    if st.button("🚀 Predict Tomorrow's BTC Price", type="primary", use_container_width=True):
        
        # --- PREDICTION LOGIC ---
        try:
            # 1. Collect inputs into a 2D array in the correct feature order
            # Order from notebook: ETH_Close, BNB_Close, SOL_Close, ADA_Close
            input_features = np.array([[
                eth_close,
                bnb_close,
                sol_close,
                ada_close
            ]])

            # 2. Scale the input features using the loaded scaler
            scaled_features = scaler.transform(input_features)

            # 3. Make prediction
            prediction = model.predict(scaled_features)

            # 4. Display the prediction
            st.subheader("Prediction Result")
            st.success(f"The predicted closing price for Bitcoin tomorrow is: **${prediction[0]:,.2f}**")
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
else:
    st.warning("The application cannot make predictions because the model or scaler files are missing.")

