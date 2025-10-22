import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

# Set page config for a cleaner look
st.set_page_config(page_title="Loan Predictor", page_icon="💰", layout="wide")

@st.cache_resource
def get_model():
    """
    Loads data, preprocesses it, and trains a Logistic Regression model.
    This function is cached so it only runs once.
    """
    # Load the dataset
    try:
        df = pd.read_csv("Loan_Data.csv")
    except FileNotFoundError:
        st.error("Error: 'Loan_Data.csv' not found. Please make sure it's in the same directory.")
        return None, None

    # --- Start Preprocessing (replicating notebook logic) ---

    # Drop Loan_ID as it's not a feature
    if 'Loan_ID' in df.columns:
        df = df.drop('Loan_ID', axis=1)

    # Fill missing values (imputation)
    # Categorical features: Fill with mode
    for col in ['Gender', 'Married', 'Dependents', 'Self_Employed', 'Credit_History']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])
            
    # Numerical features: Fill with median (less sensitive to outliers)
    for col in ['LoanAmount', 'Loan_Amount_Term']:
         if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Handle '3+' in Dependents
    if 'Dependents' in df.columns:
        df['Dependents'] = df['Dependents'].replace('3+', '3')
        # Convert to numeric
        df['Dependents'] = pd.to_numeric(df['Dependents'])

    # --- Feature Engineering & Encoding ---
    
    # Map target variable
    if 'Loan_Status' in df.columns:
        df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    else:
        st.error("Target variable 'Loan_Status' not found in CSV.")
        return None, None

    # Get dummy variables for categorical features
    # We use drop_first=True to avoid multicollinearity
    df = pd.get_dummies(df, drop_first=True)
    
    # Define Features (X) and Target (y)
    X = df.drop('Loan_Status', axis=1)
    y = df['Loan_Status']
    
    # --- Model Training ---
    
    # We scale the data as Logistic Regression benefits from it
    # We create and "save" the scaler to use on new inputs
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train the Logistic Regression model
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y)
    
    # We need to return the model, scaler, and the columns used for training
    return model, scaler, list(X.columns)

# Load the trained model, scaler, and column list
model, scaler, trained_columns = get_model()

# --- Streamlit Frontend ---

st.title("Loan Approval Predictor 💰🏦")
st.markdown("Enter the applicant's details below to see a prediction!")

if model:
    # Use columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Personal Info 🧑‍💻")
        gender = st.selectbox("Gender", ("Male", "Female"))
        married = st.selectbox("Married", ("Yes", "No"))
        dependents = st.selectbox("Dependents", ("0", "1", "2", "3"))
        education = st.selectbox("Education", ("Graduate", "Not Graduate"))
        self_employed = st.selectbox("Self Employed", ("Yes", "No"))

    with col2:
        st.subheader("Financial Info 📈")
        applicant_income = st.number_input("Applicant Income ($)", min_value=0, value=5400)
        coapplicant_income = st.number_input("Coapplicant Income ($)", min_value=0, value=1600)
        loan_amount = st.number_input("Loan Amount (in thousands $)", min_value=10, value=128)
        loan_amount_term = st.number_input("Loan Term (Months)", min_value=12, value=360)
        credit_history = st.selectbox("Credit History Available?", (1.0, 0.0), format_func=lambda x: "Yes" if x == 1.0 else "No")
        property_area = st.selectbox("Property Area", ("Urban", "Semiurban", "Rural"))

    # --- Prediction Button & Logic ---
    st.divider()
    
    if st.button("Predict Loan Status 🤞", type="primary", use_container_width=True):
        
        # 1. Create a dictionary from the inputs
        input_data = {
            'Dependents': int(dependents),
            'ApplicantIncome': applicant_income,
            'CoapplicantIncome': coapplicant_income,
            'LoanAmount': loan_amount,
            'Loan_Amount_Term': loan_amount_term,
            'Credit_History': credit_history,
            'Gender_Male': 1 if gender == "Male" else 0,
            'Married_Yes': 1 if married == "Yes" else 0,
            'Education_Not Graduate': 1 if education == "Not Graduate" else 0,
            'Self_Employed_Yes': 1 if self_employed == "Yes" else 0,
            'Property_Area_Semiurban': 1 if property_area == "Semiurban" else 0,
            'Property_Area_Urban': 1 if property_area == "Urban" else 0
        }
        
        # 2. Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # 3. Ensure columns match the training data
        # Reindex to add any missing dummy columns (filled with 0)
        input_df = input_df.reindex(columns=trained_columns, fill_value=0)
        
        # 4. Scale the input data using the saved scaler
        input_scaled = scaler.transform(input_df)
        
        # 5. Make prediction
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)[0][1] # Probability of 'Yes'

        # 6. Display the result
        if prediction[0] == 1:
            st.success(f"🎉 **Approved!** (Confidence: {probability*100:.2f}%)")
            st.balloons()
        else:
            st.error(f"😞 **Rejected.** (Confidence: {(1-probability)*100:.2f}%)")

else:
    st.warning("Model could not be loaded. Please check the CSV file and app code.")
