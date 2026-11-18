# ==============================================================================
# PHASE 3: FEATURE ENGINEERING
# ==============================================================================
# This script loads the preprocessed text data and converts it into a numerical
# format using the TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
# technique.
#
# The steps are:
#   1. Load the 'processed_text_dataset.csv'.
#   2. Split the data into training (80%) and testing (20%) sets.
#   3. Initialize a TfidfVectorizer with appropriate parameters.
#   4. Fit the vectorizer on the training text data to learn the vocabulary.
#   5. Transform both the training and testing text data into TF-IDF matrices.
#   6. Save the resulting matrices and labels for the next phase (model training).
# ==============================================================================

import pandas as pd
import os
import joblib
from scipy.sparse import save_npz
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# --- Configuration ---
DATA_DIR = "text_classification_datasets"
INPUT_CSV_PATH = os.path.join(DATA_DIR, "processed_text_dataset.csv")

# Output paths for the engineered features
X_TRAIN_PATH = os.path.join(DATA_DIR, "X_train_tfidf.npz")
X_TEST_PATH = os.path.join(DATA_DIR, "X_test_tfidf.npz")
Y_TRAIN_PATH = os.path.join(DATA_DIR, "y_train.joblib")
Y_TEST_PATH = os.path.join(DATA_DIR, "y_test.joblib")

# --- Main Execution Block ---
if __name__ == '__main__':
    print("="*60)
    print("         STARTING PHASE 3: FEATURE ENGINEERING")
    print("="*60)

    # --- Load the Preprocessed Dataset ---
    print(f"Loading preprocessed data from '{INPUT_CSV_PATH}'...")
    if not os.path.exists(INPUT_CSV_PATH):
        print(f"Error: Input file not found at '{INPUT_CSV_PATH}'.")
        print("Please ensure you have run the preprocessing script successfully.")
    else:
        df = pd.read_csv(INPUT_CSV_PATH)
        df.dropna(subset=['processed_text'], inplace=True) # Ensure no empty text rows
        print(f"Successfully loaded {len(df)} documents.")

        # Define features (X) and target (y)
        X = df['processed_text']
        y = df['category']

        # --- Split Data into Training and Testing Sets ---
        print("\nSplitting data into training (80%) and testing (20%) sets...")
        # test_size=0.2 means 20% of the data will be used for testing.
        # random_state=42 ensures that the split is the same every time we run the script.
        # stratify=y ensures that the proportion of categories is the same in both train and test sets.
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print("Data splitting complete.")
        print(f"Training set size: {len(X_train)} documents.")
        print(f"Testing set size: {len(X_test)} documents.")

        # --- TF-IDF Vectorization ---
        print("\nPerforming TF-IDF Vectorization...")
        # Initialize the TfidfVectorizer.
        # max_features=5000 means we'll only consider the top 5000 most frequent words.
        # This helps to keep the feature space manageable and removes very rare words.
        # ngram_range=(1, 2) means we will consider both single words (unigrams)
        # and pairs of adjacent words (bigrams) as features. E.g., "new york".
        tfidf_vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))

        # Fit the vectorizer on the TRAINING data and transform it.
        # This step learns the vocabulary from the training data.
        X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
        
        # ONLY transform the TESTING data using the already-fitted vectorizer.
        # This ensures that the test set is treated as unseen data.
        X_test_tfidf = tfidf_vectorizer.transform(X_test)
        print("TF-IDF Vectorization complete.")
        print(f"Shape of training feature matrix: {X_train_tfidf.shape}")
        print(f"Shape of testing feature matrix: {X_test_tfidf.shape}")

        # --- Save the Results ---
        print("\n" + "="*60)
        print("Saving the engineered features and labels...")

        # Save the sparse TF-IDF matrices
        save_npz(X_TRAIN_PATH, X_train_tfidf)
        save_npz(X_TEST_PATH, X_test_tfidf)
        print(f"Saved TF-IDF matrices to '{X_TRAIN_PATH}' and '{X_TEST_PATH}'.")

        # Save the corresponding labels using joblib
        joblib.dump(y_train, Y_TRAIN_PATH)
        joblib.dump(y_test, Y_TEST_PATH)
        print(f"Saved labels to '{Y_TRAIN_PATH}' and '{Y_TEST_PATH}'.")
        
        # Save the fitted vectorizer itself for later use (e.g., in deployment)
        vectorizer_path = os.path.join(DATA_DIR, "tfidf_vectorizer.joblib")
        joblib.dump(tfidf_vectorizer, vectorizer_path)
        print(f"Saved the fitted TF-IDF vectorizer to '{vectorizer_path}'.")

        print("\nFeature engineering phase complete!")