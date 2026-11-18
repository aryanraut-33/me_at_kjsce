# ==============================================================================
# PHASE 5: DEPLOYMENT WITH A SIMPLE GUI
# ==============================================================================
# This script creates an interactive web application using Streamlit to serve
# the trained text classification model.
#
# The app will:
#   1. Load the saved TF-IDF vectorizer and the trained Logistic Regression model.
#   2. Provide a user interface with a text area for input.
#   3. Preprocess the user's input text in the same way as the training data.
#   4. Use the model to predict the category of the input text.
#   5. Display the predicted category and the model's confidence scores.
# ==============================================================================

import streamlit as st
import joblib
import os
import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# --- Configuration ---
# Define paths to the saved model and vectorizer
# These files must exist in the specified directory
DATA_DIR = "text_classification_datasets"
MODEL_PATH = os.path.join(DATA_DIR, "logistic_regression_model.joblib")
VECTORIZER_PATH = os.path.join(DATA_DIR, "tfidf_vectorizer.joblib")

# --- Initialize NLP Tools for Preprocessing ---
# This ensures consistency with the training phase
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# --- Text Preprocessing Function ---
# This function MUST be identical to the one used in `preprocess_data.py`
def preprocess_text(text):
    """Cleans and preprocesses a single text document."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    tokens = word_tokenize(text)
    processed_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()]
    return " ".join(processed_tokens)

# --- Load Model and Vectorizer ---
# Use st.cache_resource to load these objects only once, improving app performance
@st.cache_resource
def load_model_and_vectorizer():
    """Loads the pre-trained model and TF-IDF vectorizer."""
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        return model, vectorizer
    except FileNotFoundError:
        st.error(f"Error: Model or vectorizer not found. Please ensure the files '{MODEL_PATH}' and '{VECTORIZER_PATH}' exist.")
        return None, None

model, vectorizer = load_model_and_vectorizer()

# --- Streamlit App Interface ---

st.set_page_config(page_title="Document Classifier", layout="wide")

# Title and description
st.title("📄 Document Category Classifier")
st.markdown(
    "Enter a piece of text from a document below, and the machine learning model will predict its category. "
    "The model is trained to classify text into one of four categories: **Academic**, **Book/Novel**, **Legal/Government**, or **News/Media/Magazine**."
)

st.divider()

# User input text area
st.subheader("Enter Document Text Here:")
document_text = st.text_area(
    "Paste the content of the document here. For best results, use a paragraph or more.",
    height=250,
    placeholder="e.g., 'The study found a significant correlation between the two variables...'"
)

# Classify button
if st.button("Classify Document", type="primary"):
    if model is not None and vectorizer is not None:
        if document_text.strip():
            # --- Prediction Logic ---
            
            # 1. Preprocess the input text
            processed_text = preprocess_text(document_text)
            
            # 2. Vectorize the processed text using the loaded TF-IDF vectorizer
            text_vector = vectorizer.transform([processed_text])
            
            # 3. Make a prediction using the loaded model
            prediction = model.predict(text_vector)
            
            # 4. Get prediction probabilities (confidence scores)
            prediction_proba = model.predict_proba(text_vector)
            
            # --- Display the Results ---
            st.success(f"**Predicted Category:** `{prediction[0]}`")
            
            st.subheader("Confidence Scores:")
            
            # Create a DataFrame for better visualization of probabilities
            proba_df = pd.DataFrame(
                prediction_proba,
                columns=model.classes_,
                index=["Probability"]
            ).T
            
            proba_df = proba_df.sort_values(by="Probability", ascending=False)
            proba_df['Probability'] = proba_df['Probability'].apply(lambda x: f"{x:.2%}")
            
            st.table(proba_df)

        else:
            st.warning("Please enter some text to classify.")