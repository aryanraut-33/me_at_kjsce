# ==============================================================================
# DATA BALANCING SCRIPT
# ==============================================================================
# This script fixes the class imbalance in the collected dataset by
# undersampling the majority classes.
# ==============================================================================

import pandas as pd
import os

# --- Configuration ---
DATA_DIR = "text_classification_datasets"
INPUT_CSV_PATH = os.path.join(DATA_DIR, "full_text_dataset.csv")
OUTPUT_CSV_PATH = os.path.join(DATA_DIR, "full_text_dataset_balanced.csv")

if __name__ == '__main__':
    print("="*60)
    print("         STARTING DATA BALANCING")
    print("="*60)

    # Load the original, imbalanced dataset
    df = pd.read_csv(INPUT_CSV_PATH)
    print("Original dataset loaded.")
    print("\n--- Original Class Distribution ---")
    print(df['category'].value_counts())

    # Find the size of the smallest class
    min_class_size = df['category'].value_counts().min()
    print(f"\nSmallest class has {min_class_size} samples. Balancing to this size.")

    # Undersample the other classes to match the smallest class size
    balanced_df = df.groupby('category').sample(n=min_class_size, random_state=42).reset_index(drop=True)

    print("\n--- New Balanced Class Distribution ---")
    print(balanced_df['category'].value_counts())

    # Save the new balanced DataFrame
    balanced_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print(f"\nBalanced dataset saved successfully to '{OUTPUT_CSV_PATH}'")