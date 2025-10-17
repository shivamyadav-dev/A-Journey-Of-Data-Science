import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="USA Housing Price Predictor",
    page_icon="🏠",
    layout="wide",
)

# --- CUSTOM CSS FOR A MORE APPEALING LOOK ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* General Body Styling */
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
        color: #ffffff; /* Set default text color to white for dark theme */
    }

    /* Main App background */
    .stApp {
        background-color: #1a1a2e;
        background-image: linear-gradient(to right top, #16222a, #1a2b34, #1d353f, #1f3e4a, #214855);
    }

    /* Main container with the three columns */
    .st-emotion-cache-1522cost { /* Class for the main st.container */
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Header styling */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }

    /* Prediction Button */
    .stButton>button {
        background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 1.6rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(49, 196, 190, 0.75);
    }
    .stButton>button:hover {
        background-image: linear-gradient(to right, #2575fc 0%, #6a11cb 100%);
        box-shadow: 0 6px 20px 0 rgba(49, 196, 190, 0.95);
        transform: translateY(-2px);
    }

    /* Custom box for the final prediction (Kept light for contrast) */
    .prediction-box {
        background-color: #eaf7ff;
        border: 2px dashed #aed6f1;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin-top: 2rem;
    }

    /* Model Insights boxes (success, info, warning) */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
    }
</style>
""", unsafe_allow_html=True)


# --- LOAD DATA & MODELS ---
@st.cache_data
def load_data():
    data = pd.read_csv('USA_Housing.csv')
    return data

df = load_data()

@st.cache_data
def load_results():
    try:
        results_df = pd.read_csv('model evaluation.csv')
        results_df.columns = [col.strip().upper() for col in results_df.columns]
        if 'MODEL' in results_df.columns:
            results_df = results_df.rename(columns={'MODEL': 'MODEL NAME'})
        return results_df
    except FileNotFoundError:
        return None

results_df = load_results()

@st.cache_resource
def load_model(model_name):
    try:
        with open(f'{model_name}.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        return None

# --- HEADER ---
st.title('🏠✨ USA Housing Price Predictor ✨')
st.markdown("Your journey to an instant, AI-powered home valuation starts here! 🚀")

# --- MAIN APP LAYOUT ---
with st.container(border=True):
    col1, col2, col3 = st.columns([2, 1.5, 2])

    # --- COLUMN 1: INPUT FEATURES ---
    with col1:
        st.header("⚙️ Step 1: Adjust Features")
        income = st.slider('💵 Avg. Area Income ($)', int(df['Avg. Area Income'].min()), int(df['Avg. Area Income'].max()), int(df['Avg. Area Income'].mean()))
        house_age = st.slider('🕰️ Avg. House Age (Years)', int(df['Avg. Area House Age'].min()), int(df['Avg. Area House Age'].max()), int(df['Avg. Area House Age'].mean()))
        rooms = st.slider('🛋️ Avg. Number of Rooms', int(df['Avg. Area Number of Rooms'].min()), int(df['Avg. Area Number of Rooms'].max()), int(df['Avg. Area Number of Rooms'].mean()))
        bedrooms = st.slider('🛏️ Avg. Number of Bedrooms', int(df['Avg. Area Number of Bedrooms'].min()), int(df['Avg. Area Number of Bedrooms'].max()), int(df['Avg. Area Number of Bedrooms'].mean()))
        population = st.slider('👨‍👩‍👧‍👦 Area Population', int(df['Area Population'].min()), int(df['Area Population'].max()), int(df['Area Population'].mean()))

    # --- COLUMN 2: MODEL SELECTION & PREDICTION ---
    with col2:
        st.header("🧠 Step 2: Predict")
        model_options = [
            "LassoRegression", "LinearRegression", "RidgeRegression", "PolynomialRegression",
            "ElesticNetRegression", "RandomForestRegression", "xgboostRegression", "lightgbmRegression",
            "KNeighborsRegression", "MLPRegression", "SVR", "HuberReression", "SGDRegression"
        ]
        selected_model_name = st.selectbox('🤖 Choose Your AI Brain', model_options, index=0)

        if 'predicted_price' not in st.session_state:
            st.session_state.predicted_price = "Click 'Predict' to see result"
            st.session_state.model_used = ""

        if st.button('✨ Predict House Price!', key='predict_button'):
            model = load_model(selected_model_name)
            if model:
                input_data = np.array([[income, house_age, rooms, bedrooms, population]])
                prediction = model.predict(input_data)
                st.session_state.predicted_price = f"${prediction[0]:,.2f}"
                st.session_state.model_used = f"(using {selected_model_name})"
            else:
                st.error(f"Could not load '{selected_model_name}.pkl'.")

        st.markdown(f"""
        <div class="prediction-box">
            <p style="font-size: 1.1rem; font-weight: 600; color: #555;">💰 Estimated Price</p>
            <p style="font-size: 2.5rem; font-weight: 700; color: #2980b9;">{st.session_state.predicted_price}</p>
            <p style="font-size: 0.9rem; color: #777;">{st.session_state.model_used}</p>
        </div>
        """, unsafe_allow_html=True)

    # --- COLUMN 3: MODEL INSIGHTS (DYNAMIC) ---
    with col3:
        st.header("📊 Step 3: AI Report Card")
        if results_df is not None and not results_df.empty:
            results_df['R2'] = pd.to_numeric(results_df['R2'], errors='coerce')
            results_df['MAE'] = pd.to_numeric(results_df['MAE'], errors='coerce')
            results_df_sorted = results_df.sort_values(by='R2', ascending=False).dropna()

            if not results_df_sorted.empty:
                best_model_row = results_df_sorted.iloc[0]
                model_stats = results_df[results_df['MODEL NAME'].str.strip() == selected_model_name.strip()]

                if not model_stats.empty:
                    model_stats = model_stats.iloc[0]
                    model_r2 = model_stats['R2']
                    model_mae = model_stats['MAE']

                    st.write(f"You've selected **{selected_model_name}**. Here's its performance review:")

                    mcol1, mcol2 = st.columns(2)
                    mcol1.metric("🎯 Accuracy Score", f"{model_r2:.3f}")
                    mcol2.metric("💲 Avg. Error", f"${model_mae:,.0f}")

                    if model_r2 >= best_model_row['R2'] * 0.98:
                        st.success(f"⭐ **Excellent Choice:** This AI is a top performer, providing highly reliable predictions!")
                    elif model_r2 > 0.85:
                        st.info(f"👍 **Good Choice:** This AI is a solid performer and reliable for most predictions.")
                    else:
                        st.warning(f"🤔 **Use with Caution:** This AI is less reliable and may have a higher prediction error.")
                else:
                    st.error(f"No performance data found for '{selected_model_name}'.")
            else:
                st.warning("Could not analyze model performance from the results file.")
        else:
            st.error("Could not find 'model evaluation.csv' file.")

