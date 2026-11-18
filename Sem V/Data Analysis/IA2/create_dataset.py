# ==============================================================================
# DATA COLLECTION AND BALANCING SCRIPT
# ==============================================================================
# This script performs two key functions:
# 1. Extracts ONLY the main content from the specified Kaggle datasets for each
#    of the four categories.
# 2. Balances the dataset by undersampling the larger categories to match the
#    size of the smallest category, ensuring all four classes are present.
#
# This script is the definitive starting point for the project pipeline.
# ==============================================================================

import os
import pandas as pd
import kaggle
import re

# --- Configuration ---
DATA_DIR = "text_classification_datasets"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# The final output file that the rest of the pipeline will use
OUTPUT_CSV_PATH = os.path.join(DATA_DIR, "full_text_dataset.csv")

# ==============================================================================
# HELPER AND DATA COLLECTION FUNCTIONS
# ==============================================================================

def download_and_extract_kaggle_dataset(dataset_name, target_dir):
    """Checks if data exists, otherwise downloads and unzips from Kaggle."""
    if not os.path.exists(target_dir) or not os.listdir(target_dir):
        print(f"Downloading Kaggle dataset: {dataset_name}...")
        os.makedirs(target_dir, exist_ok=True)
        try:
            kaggle.api.dataset_download_files(dataset_name, path=target_dir, unzip=True)
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading {dataset_name}: {e}")
            return False
    else:
        print(f"Dataset '{dataset_name}' already exists in {target_dir}.")
    return True

def collect_academic_data():
    """Extracts main content (Title + Abstract) for the 'Academic' category."""
    print("\n--- Collecting Academic Data ---")
    dataset_name = 'devintheai/arxiv-cs-papers-multi-label-classification-200k-v1'
    target_dir = os.path.join(DATA_DIR, 'arxiv_cs_papers')
    if not download_and_extract_kaggle_dataset(dataset_name, target_dir): return []
    
    df = pd.read_csv(os.path.join(target_dir, 'cs_papers_api.csv'))
    # Combine title and abstract to form the main content
    df['text'] = df['title'] + ". " + df['abstract']
    return [{'text': text, 'category': 'Academic'} for text in df['text'].dropna()]

def collect_legal_government_data():
    """Extracts main content (Judgement) for the 'Legal/Government' category."""
    print("\n--- Collecting Legal/Government Data ---")
    dataset_name = 'veerchheda/civilsum-indian-legal-document-summarisation'
    target_dir = os.path.join(DATA_DIR, 'civilsum_legal')
    if not download_and_extract_kaggle_dataset(dataset_name, target_dir): return []

    df = pd.read_csv(os.path.join(target_dir, 'train.csv'))
    # The 'Judgement ' column is the main content
    df.rename(columns={'Judgement ': 'text'}, inplace=True)
    return [{'text': text, 'category': 'Legal/Government'} for text in df['text'].dropna()]

def collect_book_novel_data():
    """
    CORRECTED: Extracts main content using the correct column names:
    - 'PlayerLine' for the text.
    - 'ActSceneLine' to determine the Act for grouping.
    """
    print("\n--- Collecting Book/Novel Data (Corrected) ---")
    dataset_name = 'kingburrito666/shakespeare-plays'
    target_dir = os.path.join(DATA_DIR, 'shakespeare_plays')
    if not download_and_extract_kaggle_dataset(dataset_name, target_dir): return []

    try:
        csv_path = os.path.join(target_dir, 'Shakespeare_data.csv')
        df = pd.read_csv(csv_path)

        # Drop rows with no text or scene information
        df.dropna(subset=['PlayerLine', 'ActSceneLine'], inplace=True)
        
        # Extract the Act number (the first digit) from the 'ActSceneLine' column
        df['Act'] = df['ActSceneLine'].apply(lambda x: str(x).split('.')[0])
        
        # Group by the Play and the new 'Act' column, then join the 'PlayerLine' text
        df_grouped = df.groupby(['Play', 'Act'])['PlayerLine'].apply(' '.join).reset_index()
        
        return [{'text': text, 'category': 'Book/Novel'} for text in df_grouped['PlayerLine'].dropna()]

    except Exception as e:
        print(f"An error occurred while processing the Shakespeare dataset: {e}")
        return []
def collect_news_media_data():
    """Extracts main content (Title + Content) for the 'News/Media/Magazine' category."""
    print("\n--- Collecting News/Media/Magazine Data ---")
    dataset_name = 'hgultekin/bbcnewsarchive'
    target_dir = os.path.join(DATA_DIR, 'bbc_news')
    if not download_and_extract_kaggle_dataset(dataset_name, target_dir): return []
        
    df = pd.read_csv(os.path.join(target_dir, 'bbc-news-data.csv'), sep='\t')
    # Combine title and content to form the main content
    df['text'] = df['title'] + ". " + df['content']
    return [{'text': text, 'category': 'News/Media/Magazine'} for text in df['text'].dropna()]

# ==============================================================================
# MAIN ORCHESTRATOR
# ==============================================================================

if __name__ == '__main__':
    all_data = []

    print("="*60)
    print("      STARTING CORRECTED DATA COLLECTION & BALANCING")
    print("="*60)

    # Step 1: Collect data from all four sources
    all_data.extend(collect_academic_data())
    all_data.extend(collect_legal_government_data())
    all_data.extend(collect_book_novel_data())
    all_data.extend(collect_news_media_data())

    # Step 2: Create a DataFrame and perform initial cleaning
    df = pd.DataFrame(all_data)
    df.dropna(subset=['text'], inplace=True)
    df['text'] = df['text'].astype(str).apply(lambda x: re.sub(r'\s+', ' ', x).strip())
    df = df[df['text'].str.len() > 50].copy()
    df.drop_duplicates(subset=['text'], inplace=True)

    print("\n\n" + "="*60)
    print("      BALANCING THE DATASET")
    print("="*60)
    
    print("\n--- Original Class Distribution ---")
    print(df['category'].value_counts())

    # Step 3: Balance the dataset by undersampling
    min_class_size = df['category'].value_counts().min()
    print(f"\nSmallest class has {min_class_size} samples. Balancing all classes to this size.")

    balanced_df = df.groupby('category').sample(n=min_class_size, random_state=42)

    # Step 4: Shuffle the balanced dataset
    balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

    print("\n--- New Balanced Class Distribution ---")
    print(balanced_df['category'].value_counts())

    # Step 5: Save the final, clean, and balanced dataset
    balanced_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print(f"\nSUCCESS: Clean and balanced dataset saved to '{OUTPUT_CSV_PATH}'")
    print("You can now proceed with the rest of the pipeline (preprocess, feature_engineering, etc.).")