import streamlit as st
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pickle
import time

# Page Configuration
st.set_page_config(
    page_title="Restaurant Review Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #7c2d12 75%, #1c1917 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    h1, h2, h3 {
        color: white !important;
    }
    
    .stMarkdown {
        color: white;
    }
    
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    .stSelectbox select {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .result-positive {
        background: rgba(34, 197, 94, 0.2);
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .result-negative {
        background: rgba(239, 68, 68, 0.2);
        border: 2px solid #ef4444;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .developer-credit {
        text-align: center;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .developer-name {
        font-size: 18px;
        font-weight: bold;
        background: linear-gradient(45deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 5px 0;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize NLTK
@st.cache_resource
def initialize_nltk():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    return PorterStemmer(), set(stopwords.words('english'))

# Load model and vectorizer
@st.cache_resource
def load_model_and_vectorizer():
    try:
        with open("best_model.pkl", 'rb') as f:
            model = pickle.load(f)
        with open("vectorizer.pkl", 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please ensure 'best_model.pkl' and 'vectorizer.pkl' are in the same directory.")
        return None, None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Text preprocessing
def preprocess_text(text, ps, stopwords_set):
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower().split()
    review = [ps.stem(word) for word in review if word not in stopwords_set]
    return ' '.join(review)

# Analyze sentiment
def analyze_sentiment(user_input, model, vectorizer, ps, stopwords_set):
    if not user_input.strip():
        return None, None, None
    
    cleaned_review = preprocess_text(user_input, ps, stopwords_set)
    review_vector = vectorizer.transform([cleaned_review]).toarray()
    
    prediction = int(model.predict(review_vector)[0])
    probabilities = model.predict_proba(review_vector)[0]
    confidence = probabilities[prediction] * 100
    
    return prediction, probabilities, confidence

# Display result card
def display_result(prediction, probabilities, confidence):
    if prediction == 1:
        st.markdown(f"""
            <div class='result-positive'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <div style='font-size: 40px;'>👍</div>
                    <div>
                        <h4 style='color: #86efac; margin: 0;'>😊 Positive</h4>
                        <p style='color: #86efac; margin: 5px 0; font-size: 14px;'>{confidence:.2f}%</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='result-negative'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <div style='font-size: 40px;'>👎</div>
                    <div>
                        <h4 style='color: #fca5a5; margin: 0;'>😞 Negative</h4>
                        <p style='color: #fca5a5; margin: 5px 0; font-size: 14px;'>{confidence:.2f}%</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 12px; margin: 15px 0 5px 0;'>Confidence Level</p>", unsafe_allow_html=True)
    st.progress(confidence / 100)
    
    st.markdown("<p style='font-size: 12px; margin: 15px 0 10px 0;'>Probability Breakdown</p>", unsafe_allow_html=True)
    
    col1_res, col2_res = st.columns(2)
    
    negative_prob = probabilities[0] * 100
    positive_prob = probabilities[1] * 100
    
    with col1_res:
        st.markdown(f"""
            <div class='metric-card' style='border-left: 4px solid #ef4444;'>
                <p style='color: #fca5a5; margin: 0; font-size: 12px;'>Negative</p>
                <h3 style='color: white; margin: 8px 0;'>{negative_prob:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col2_res:
        st.markdown(f"""
            <div class='metric-card' style='border-left: 4px solid #22c55e;'>
                <p style='color: #86efac; margin: 0; font-size: 12px;'>Positive</p>
                <h3 style='color: white; margin: 8px 0;'>{positive_prob:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)

# Main app
def main():
    st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>🍽️ Restaurant Review Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d1d5db; font-size: 16px; margin-bottom: 20px;'>Predict customer sentiment using AI</p>", unsafe_allow_html=True)
    
    ps, all_stopwords = initialize_nltk()
    model, vectorizer = load_model_and_vectorizer()
    
    if model is None or vectorizer is None:
        st.stop()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    sample_reviews = [
        "The food was absolutely amazing! Best restaurant I've ever been to.",
        "Terrible service and the food was cold. Never coming back.",
        "Outstanding ambiance and delicious dishes. Highly recommend!",
        "Worst meal ever. Overpriced and tasteless.",
        "Great experience! Will definitely come back."
    ]
    
    with col1:
        
        st.markdown("<h3 style='margin-top: 0;'>Sample Reviews</h3>", unsafe_allow_html=True)
        selected_sample = st.selectbox(
            "Select a sample...",
            sample_reviews,
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        
        st.markdown("<h3 style='margin-top: 0;'>Your Review</h3>", unsafe_allow_html=True)
        user_input = st.text_area(
            "Review",
            value=selected_sample,
            height=100,
            placeholder="Type your restaurant review here...",
            label_visibility="collapsed"
        )
        analyze_button = st.button("🔮 Analyze Sentiment")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        
        st.markdown("<h3 style='margin-top: 0;'>Results</h3>", unsafe_allow_html=True)
        result_placeholder = st.empty()
        
        if analyze_button:
            if not user_input.strip():
                result_placeholder.warning("⚠️ Please enter a review to analyze.")
            else:
                with result_placeholder.container():
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_text.text("Analyzing your review...")
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    prediction, probabilities, confidence = analyze_sentiment(
                        user_input, model, vectorizer, ps, all_stopwords
                    )
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    if prediction is not None:
                        display_result(prediction, probabilities, confidence)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='developer-credit'>
            <p style='color: #9ca3af; font-size: 14px; margin-bottom: 5px;'>
                Developed by
            </p>
            <div class='developer-name'>
                Shivam Kumar Yadav
            </div>
            <p style='color: #6b7280; font-size: 12px; margin-top: 5px;'>
                AI-Powered Sentiment Analysis Tool
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()