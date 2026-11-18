# ==============================================================================
# PHASE 4: MODEL SELECTION AND TRAINING
# ==============================================================================
# This script loads the engineered features and trains a classical machine
# learning model for text classification.
#
# The steps are:
#   1. Load the TF-IDF training matrix (X_train) and the training labels (y_train).
#   2. Initialize a machine learning model. We will use Logistic Regression, a
#      strong and efficient baseline for this type of task.
#   3. Train the model on the data.
#   4. Save the trained model to a file for use in the evaluation phase.
# ==============================================================================

import os
import joblib
from scipy.sparse import load_npz
from sklearn.linear_model import LogisticRegression

# --- Configuration ---
DATA_DIR = "text_classification_datasets"
# Input paths for the engineered features from Phase 3
X_TRAIN_PATH = os.path.join(DATA_DIR, "X_train_tfidf.npz")
Y_TRAIN_PATH = os.path.join(DATA_DIR, "y_train.joblib")

# Output path for the trained model
MODEL_OUTPUT_PATH = os.path.join(DATA_DIR, "logistic_regression_model.joblib")


# --- Main Execution Block ---
if __name__ == '__main__':
    print("="*60)
    print("         STARTING PHASE 4: MODEL TRAINING")
    print("="*60)

    # --- Load the Training Data ---
    print("Loading training data...")
    try:
        X_train = load_npz(X_TRAIN_PATH)
        y_train = joblib.load(Y_TRAIN_PATH)
        print("Training data loaded successfully.")
        print(f"Training features shape: {X_train.shape}")
        print(f"Training labels shape: {y_train.shape}")
    except FileNotFoundError:
        print("Error: Training data not found.")
        print("Please ensure you have run the feature_engineering.py script first.")
        exit()

    # --- Initialize and Train the Model ---
    print("\nInitializing and training the Logistic Regression model...")
    # We choose Logistic Regression as our model.
    # Other great options include: MultinomialNB(), LinearSVC(), or RandomForestClassifier().
    # - random_state=42 ensures our results are reproducible.
    # - max_iter=1000 provides the solver with enough iterations to converge.
    # - multi_class='multinomial' is well-suited for multi-class problems.
    model = LogisticRegression(random_state=42, max_iter=1000, multi_class='multinomial')

    # The .fit() method is where the model learns from the data.
    # It adjusts its internal parameters to best map the TF-IDF features (X_train)
    # to the correct categories (y_train).
    model.fit(X_train, y_train)

    print("Model training complete.")

    # --- Save the Trained Model ---
    print("\n" + "="*60)
    print(f"Saving the trained model to '{MODEL_OUTPUT_PATH}'...")
    # We save the 'model' object, which now contains all the learned patterns.
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print("Model saved successfully.")

    print("\nModel training phase complete!")