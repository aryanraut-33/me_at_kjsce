# ==============================================================================
# PHASE 5: EVALUATION
# ==============================================================================
# This script evaluates the performance of the trained model on the unseen
# test data.
#
# The steps are:
#   1. Load the trained model and the test dataset (features and labels).
#   2. Make predictions on the test data.
#   3. Calculate and print key performance metrics:
#      - Accuracy Score.
#      - Detailed Classification Report (Precision, Recall, F1-Score).
#   4. Generate and display a Confusion Matrix to visualize the model's
#      performance on a per-class basis.
#   5. Save the confusion matrix plot to a file.
# ==============================================================================

import os
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import load_npz
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

import pandas as pd

# --- Configuration ---
DATA_DIR = "text_classification_datasets"
# Input paths
MODEL_PATH = os.path.join(DATA_DIR, "logistic_regression_model.joblib")
X_TEST_PATH = os.path.join(DATA_DIR, "X_test_tfidf.npz")
Y_TEST_PATH = os.path.join(DATA_DIR, "y_test.joblib")

# Output path for the confusion matrix plot
CONFUSION_MATRIX_PLOT_PATH = "confusion_matrix.png"

# --- Main Execution Block ---
if __name__ == '__main__':
    print("="*60)
    print("         STARTING PHASE 5: MODEL EVALUATION")
    print("="*60)

    # --- Load Model and Test Data ---
    print("Loading the trained model and test data...")
    try:
        model = joblib.load(MODEL_PATH)
        X_test = load_npz(X_TEST_PATH)
        y_test = joblib.load(Y_TEST_PATH)
        print("Model and test data loaded successfully.")
    except FileNotFoundError:
        print("Error: Model or test data not found.")
        print("Please ensure you have run the previous scripts successfully.")
        exit()

    # --- Make Predictions on Test Data ---
    print("\nMaking predictions on the unseen test data...")
    y_pred = model.predict(X_test)
    print("Predictions complete.")

    # --- Calculate and Display Metrics ---
    # 1. Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("\n" + "-"*60)
    print("                    PERFORMANCE METRICS")
    print("-"*60)
    print(f"Overall Accuracy: {accuracy:.4f} ({accuracy:.2%})")

    # 2. Classification Report
    print("\n--- Classification Report ---")
    # This report gives a breakdown of precision, recall, and f1-score for each class.
    # - Precision: Of all the documents the model predicted as a certain category, how many were correct?
    # - Recall: Of all the actual documents of a certain category, how many did the model correctly identify?
    # - F1-Score: The harmonic mean of precision and recall. A good overall measure.
    print(classification_report(y_test, y_pred, target_names=model.classes_))

    # 3. Confusion Matrix
    print("\n--- Confusion Matrix ---")
    # The matrix shows the counts of predicted vs. actual classes.
    # Rows represent the TRUE labels.
    # Columns represent the PREDICTED labels.
    # The diagonal (top-left to bottom-right) shows the number of correct predictions for each class.
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
    print(cm_df)

    # --- Visualize and Save the Confusion Matrix ---
    print(f"\nGenerating and saving confusion matrix plot to '{CONFUSION_MATRIX_PLOT_PATH}'...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix', fontsize=16)
    plt.ylabel('Actual Category', fontsize=12)
    plt.xlabel('Predicted Category', fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout() # Adjust layout to make room for labels
    plt.savefig(CONFUSION_MATRIX_PLOT_PATH)
    print("Plot saved successfully.")

    print("\n" + "="*60)
    print("         MODEL EVALUATION COMPLETE!")
    print("="*60)