# ==============================================================================
# PHASE 2: DATA PREPROCESSING AND CLEANING
# ==============================================================================
# This script loads the collected raw text data and performs comprehensive
# cleaning and preprocessing steps to prepare it for machine learning.
#
# The steps are:
#   1. Load the dataset from 'full_text_dataset.csv'.
#   2. Clean the text:
#      - Convert to lowercase.
#      - Remove punctuation and special characters.
#      - Remove numbers/digits.
#   3. Tokenize the text (split into words).
#   4. Remove common English stop words.
#   5. Lemmatize the tokens (reduce words to their root form).
#   6. Join tokens back into a single clean string.
#   7. Save the processed data to 'processed_text_dataset.csv'.
# ==============================================================================

import pandas as pd
import os
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# --- Configuration ---
DATA_DIR = "text_classification_datasets"
INPUT_CSV_PATH = os.path.join(DATA_DIR, "full_text_dataset.csv")
OUTPUT_CSV_PATH = os.path.join(DATA_DIR, "processed_text_dataset.csv")

# --- Initialize NLP tools ---
# We initialize these once to avoid reloading them for every row.
lemmatizer = WordNetLemmatizer()
# Create a set of English stop words for faster processing
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    """
    A comprehensive function to clean and preprocess a single text document.
    """
    # 1. Lowercasing
    # Convert all characters to lowercase to ensure uniformity.
    # Example: "The QUICK brown fox" -> "the quick brown fox"
    text = text.lower()

    # 2. Removing Punctuation
    # Remove all punctuation marks from the text.
    # We create a translation table to efficiently remove punctuation.
    # Example: "hello, world!" -> "hello world"
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 3. Removing Numbers/Digits
    # Use regular expressions to find and remove all digits.
    # Example: "There are 3 apples" -> "There are  apples"
    text = re.sub(r'\d+', '', text)

    # 4. Tokenization
    # Split the cleaned text into a list of individual words (tokens).
    # Example: "the quick brown fox" -> ["the", "quick", "brown", "fox"]
    tokens = word_tokenize(text)

    # 5. Stop Word Removal and Lemmatization
    # We process this in a single loop for efficiency.
    processed_tokens = []
    for word in tokens:
        # First, check if the word is a stop word.
        # We also check if the word contains any alphabetic characters to filter
        # out any remaining non-textual tokens (e.g., single punctuation marks
        # that were not caught).
        if word not in stop_words and word.isalpha():
            # If it's not a stop word, lemmatize it.
            # Lemmatization reduces the word to its base or dictionary form.
            # Example: "running" -> "run", "better" -> "good" (with POS tag)
            # We use a simple version here without POS tagging for speed.
            lemmatized_word = lemmatizer.lemmatize(word)
            processed_tokens.append(lemmatized_word)

    # 6. Join Tokens Back to String
    # Re-join the cleaned tokens into a single string, with spaces in between.
    # This format is ideal for feature extraction techniques like TF-IDF.
    # Example: ["quick", "brown", "fox", "jump"] -> "quick brown fox jump"
    text = " ".join(processed_tokens)
    
    return text

# --- Main Execution Block ---
if __name__ == '__main__':
    print("="*60)
    print("         STARTING PHASE 2: DATA PREPROCESSING")
    print("="*60)

    # --- Load the Dataset ---
    print(f"Loading raw data from '{INPUT_CSV_PATH}'...")
    if not os.path.exists(INPUT_CSV_PATH):
        print(f"Error: Input file not found at '{INPUT_CSV_PATH}'.")
        print("Please ensure you have run the data collection script successfully.")
    else:
        df = pd.read_csv(INPUT_CSV_PATH)
        print(f"Successfully loaded {len(df)} documents.")

        # Drop any rows that might have empty text after loading
        df.dropna(subset=['text'], inplace=True)
        df['text'] = df['text'].astype(str)

        # --- Apply the Preprocessing Function ---
        print("\nPreprocessing text data... This may take a few minutes.")
        # We create a new column 'processed_text' to store the cleaned text.
        # The .apply() method efficiently runs our function on each row of the 'text' column.
        df['processed_text'] = df['text'].apply(preprocess_text)
        print("Preprocessing complete.")

        # --- Display a Comparison ---
        print("\n--- Preprocessing Comparison ---")
        # Select one example from each category to show the before-and-after
        comparison_df = df.groupby('category').head(1).copy()
        for index, row in comparison_df.iterrows():
            print(f"\nCATEGORY: {row['category']}")
            print("-" * 20)
            print(f"ORIGINAL:\n{row['text'][:300]}...") # Show first 300 chars
            print(f"\nPROCESSED:\n{row['processed_text'][:300]}...")

        # --- Save the Processed Data ---
        print("\n" + "="*60)
        print(f"Saving processed data to '{OUTPUT_CSV_PATH}'...")
        # We save the dataframe with the new 'processed_text' column.
        # This allows us to easily load the cleaned data for the next phase.
        df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        print("Processed data saved successfully.")
        
        # Final check
        print("\n--- Final Processed DataFrame Info ---")
        df.info()
        print("\n--- Head of the Final DataFrame ---")
        print(df.head())