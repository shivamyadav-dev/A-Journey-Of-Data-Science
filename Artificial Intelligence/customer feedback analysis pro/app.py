import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import time
import pickle

# --- Page Configuration ---
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🍽️",
    layout="wide"
)

# --- Creative Background & Styling ---
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Main App Background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            background-attachment: fixed;
            color: #ffffff;
        }
        
        /* Main content area */
        [data-testid="stMain"] {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 2rem;
        }

        /* Streamlit Widgets */
        [data-testid="stTextArea"] textarea {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        [data-testid="stTextArea"] textarea:focus {
            background-color: rgba(255, 255, 255, 0.2);
            border: 1px solid #4F46E5; /* Changed from neon red */
            color: #ffffff;
        }
        [data-testid="stButton"] button {
            background: linear-gradient(45deg, #4F46E5, #7C3AED); /* Changed from neon red */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3); /* Changed from neon red */
        }
        [data-testid="stButton"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5); /* Changed from neon red */
            filter: brightness(1.1);
        }

        /* Titles and Headers */
        h1, h2, h3 {
            color: #ffffff;
        }
        
        /* Footer Styling */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0f0c29;
            color: #FAFAFA;
            text-align: center;
            padding: 10px 0;
            font-family: 'monospace';
            font-size: 0.9em;
            border-top: 1px solid #302b63;
        }
        
        /* Success/Error boxes */
        [data-testid="stSuccess"] {
            background-color: rgba(46, 139, 87, 0.3);
            border: 1px solid #2E8B57;
            border-radius: 8px;
        }
        [data-testid="stError"] {
            background-color: rgba(220, 20, 60, 0.3);
            border: 1px solid #DC143C;
            border-radius: 8px;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

add_custom_css()

# --- NLTK Resources ---
# Initialize stemmer and download stopwords
nltk.download('stopwords')
ps = PorterStemmer()
all_stopwords = set(stopwords.words('english'))


# --- Model Training Function (Cached) ---
# @st.cache_resource tells Streamlit to run this function only ONCE
# and save the result (the model, vectorizer, and accuracy).
@st.cache_resource
def train_model():
    """
    Loads data, cleans it, and trains the Logistic Regression model.
    This function is cached and runs only once.
    """
    try:
        # 1. Load dataset, explicitly stating it has NO header.
        # This forces pandas to read 'Review\tLiked' as data,
        # which is what the errors imply is happening.
        dataset = pd.read_csv("Restaurant_Reviews.tsv", delimiter="\t", quoting=3, header=None)
        
        if len(dataset.columns) < 2:
             st.error(f"FATAL ERROR: `Restaurant_Reviews.tsv` does not appear to have at least two columns.")
             st.error("Please check the file's delimiter and format.")
             return None, None, None
        
        # --- ROBUST HEADER FIX ---
        # 1. Rename columns by position (0 and 1)
        # This assumes the first row is either data or a header read as data.
        try:
            dataset = dataset.rename(columns={
                dataset.columns[0]: 'Review',
                dataset.columns[1]: 'Liked'
            })
        except Exception as e:
            st.error(f"Error renaming columns: {e}")
            st.error("This can happen if the file is empty or formatted incorrectly.")
            return None, None, None

        # 2. Check if the first row is the header (which we read as data)
        # If the 'Liked' column's first item is NOT a digit, assume it's the header.
        if not str(dataset['Liked'].iloc[0]).isdigit():
            # Drop the first row (index 0), which is the header.
            dataset = dataset.iloc[1:].reset_index(drop=True)
        # --- END FIX ---

    except FileNotFoundError:
        st.error("FATAL ERROR: `Restaurant_Reviews.tsv` not found.")
        st.error("Please make sure the .tsv file is in the same folder as this app.")
        return None, None, None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

    # 2. Text cleaning
    corpus = []
    # Now this will reliably find 'Review'
    for review in dataset['Review']:
        review = re.sub('[^a-zA-Z]', ' ', str(review)) # Added str() for safety
        review = review.lower().split()
        review = [ps.stem(word) for word in review if word not in all_stopwords]
        corpus.append(' '.join(review))

    # 3. Feature extraction (Bag of Words)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()
    
    # --- BUG FIX ---
    # Convert the 'Liked' column to integers (was being read as strings)
    # This ensures the model predicts 0/1 as numbers, not "0"/"1" as text.
    try:
        # Now this will reliably find 'Liked' and it will only contain numbers.
        y = dataset['Liked'].astype(int)
    except KeyError:
        # This error should no longer happen due to the renaming fix above.
        st.error(f"FATAL ERROR: 'Liked' column not found. Found columns: {list(dataset.columns)}.")
        return None, None, None
    except ValueError:
        # This error should no longer happen.
        st.error("FATAL ERROR: 'Liked' column contains non-numeric values.")
        st.error("This is an unexpected error after attempting to clean the header.")
        return None, None, None
    # --- END FIX ---


    # 4. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Train Logistic Regression
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # 6. Calculate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, vectorizer, accuracy

# --- Text Preprocessing Function (for live input) ---
def preprocess_text(text):
    """
    Cleans and preprocesses a single text review from the user.
    """
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower().split()
    review = [ps.stem(word) for word in review if word not in all_stopwords]
    review = ' '.join(review)
    return review

# --- Main App ---
st.title("🍽️ Restaurant Review Sentiment Analyzer")

# Load (or train) the model
with st.spinner("Warming up the AI model... This may take a moment on first run."):
    model, vectorizer, accuracy = train_model()

if model and vectorizer and accuracy:
    st.markdown(f"Enter a review to predict if it's **Positive (Liked)** or **Negative (Not Liked)**.")
    st.markdown(f"This app uses a **Logistic Regression** model with a trained accuracy of **{accuracy*100:.2f}%**.")

    col1, col2 = st.columns([2, 1])

    with col1:
        user_input = st.text_area(
            "Enter your review:", 
            height=200, 
            placeholder="The food was amazing, and the service was even better!"
        )

        if st.button("Analyze Sentiment", use_container_width=True):
            if user_input.strip():
                # 1. Preprocess live text
                cleaned_review = preprocess_text(user_input)
                
                # 2. Vectorize live text
                review_vector = vectorizer.transform([cleaned_review]).toarray()
                
                # 3. Predict
                prediction = model.predict(review_vector)
                probability = model.predict_proba(review_vector)
                
                # --- ERROR FIX ---
                # Cast prediction[0] (which is numpy.int) to a standard int
                # to safely index the probability array.
                predicted_class_index = int(prediction[0])
                prob_percent = probability[0][predicted_class_index] * 100
                # --- END FIX ---
                
                # 4. Display Result
                with st.spinner('Analyzing...'):
                    time.sleep(1) # Add a small delay for effect
                    with col2:
                        st.subheader("Analysis Result")
                        if prediction[0] == 1:
                            st.success(f"### 😊 Positive Review")
                            st.write(f"We are **{prob_percent:.2f}%** confident this is a **positive** review.")
                            st.balloons()
                        else:
                            st.error(f"### 😞 Negative Review")
                            st.write(f"We are **{prob_percent:.2f}%** confident this is a **negative** review.")
            else:
                st.warning("Please enter a review to analyze.")

# --- Developer Credit Footer ---
st.markdown(
    """
    <div class="footer">
        ✨ A creative frontend developed by <b>Shivam Kumar Yadav</b> ✨
    </div>
    """,
    unsafe_allow_html=True
)

