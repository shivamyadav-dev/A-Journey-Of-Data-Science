import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


st.set_page_config(
    page_title="Startup Profit Predictor",
    page_icon="💰",
    layout="wide"
)


def train_model(df):
    
    """Preprocesses data and trains a Linear Regression model."""
    
    # Define features (X) and target (y)
    # The first 4 columns are features, the last one is the target
    X = df.iloc[:, :-1]
    y = df.iloc[:, 4]

    # One-Hot Encode the 'State' column
    # This converts categorical data (cities) into a numerical format
    X = pd.get_dummies(X, columns=['State'], drop_first=True, dtype=int)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Create and train the Linear Regression model
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Return all necessary components for prediction and evaluation
    return regressor, X_train, X_test, y_train, y_test, X.columns

# --- Main Application Logic ---

# --- Header ---
st.title("💰 Startup Profit Predictor")
st.markdown("This app uses a Multiple Linear Regression model to predict the profit of a startup based on its spending in different areas.")

# --- Load Data ---
try:
    dataset = pd.read_csv("Investment.csv")
    st.success("Dataset loaded successfully!")
    
    # Train the model using the cached function
    regressor, X_train, X_test, y_train, y_test, feature_columns = train_model(dataset)

    # --- Sidebar for User Input ---
    st.sidebar.header("Make a New Prediction")
    st.sidebar.markdown("Enter the spending details for a new startup.")

    # Create number inputs for spending based on new columns
    research_spend = st.sidebar.number_input("Research Spend", min_value=0.0, value=150000.0, step=1000.0, format="%.2f")
    promotion_spend = st.sidebar.number_input("Promotion Spend", min_value=0.0, value=120000.0, step=1000.0, format="%.2f")
    dm_spend = st.sidebar.number_input("Digital Marketing Spend", min_value=0.0, value=400000.0, step=1000.0, format="%.2f")
    
    # Create a select box for the state/city
    state = st.sidebar.selectbox("State", ("Hyderabad", "Bangalore", "Chennai"))
    
    if st.sidebar.button("Predict Profit", use_container_width=True):
        # --- Prediction Logic ---
        # Create a dataframe from the user's input with the correct feature columns
        input_data = pd.DataFrame(columns=feature_columns)
        input_data.loc[0] = 0 
        
        # Populate the dataframe with user input
        input_data['Research'] = research_spend
        input_data['Promotion'] = promotion_spend
        input_data['DigitalMarketing'] = dm_spend
        
        # Set the correct state column to 1
        # 'Bangalore' is dropped by get_dummies, so we only need to set flags for the others.
        if state == 'Chennai':
            input_data['State_Chennai'] = 1
        elif state == 'Hyderabad':
            input_data['State_Hyderabad'] = 1
        
        # Ensure the column order matches the training data
        input_data = input_data[feature_columns]

        # Make the prediction
        prediction = regressor.predict(input_data)
        
        # Display the prediction
        st.sidebar.success(f"Predicted Profit: ${prediction[0]:,.2f}")


    # --- Main Page Display ---
    st.header("Model Performance")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Training Score (R²)",
            value=f"{regressor.score(X_train, y_train):.4f}"
        )
        st.markdown("This score shows how well the model fits the data it was trained on.")
    with col2:
        st.metric(
            label="Testing Score (R²)",
            value=f"{regressor.score(X_test, y_test):.4f}"
        )
        st.markdown("This score shows how well the model generalizes to new, unseen data.")

    st.header("Dataset Preview")
    st.dataframe(dataset.head())

    # --- Expander for Statistical Analysis ---
    with st.expander("View Detailed Statistical Analysis (Backward Elimination)"):
        st.markdown("""
        The summary below is from a more rigorous statistical model (OLS). We use a technique called **Backward Elimination** to remove features that are not statistically significant (where P>|t| is greater than 0.05). 
        
        Based on this analysis, **Research** spend is the most significant predictor of profit.
        """)
        
        # Prepare data for statsmodels (adding a constant for the intercept)
        X_for_ols = dataset.iloc[:, :-1]
        y_for_ols = dataset.iloc[:, 4]
        X_for_ols = pd.get_dummies(X_for_ols, columns=['State'], drop_first=True, dtype=int)
        
        # After backward elimination, the optimal features are Research spend
        X_opt = X_for_ols[['Research']]
        X_opt = sm.add_constant(X_opt) # Add constant for intercept
        
        regressor_OLS = sm.OLS(endog=y_for_ols, exog=X_opt).fit()
        
        # Display the summary as text
        st.code(str(regressor_OLS.summary()))


except FileNotFoundError:
    st.error("Error: 'Investment.csv' not found. Please make sure the CSV file is in the same directory as the script.")
except Exception as e:
    st.error(f"An error occurred: {e}")

