# ISM2411 - Data Cleaning Project
# Purpose: The prpose is to clean sales data in the csv file
# handling missing data, and standardizing column names.

import pandas as pd
import os

def load_data(file_path):
    """
    Loads data from a CSV file.
    """
    # Check if file exists before loading
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
    
    return pd.read_csv(file_path)

if __name__ == "__main__":
    # Define paths
    raw_path = "data/raw/sales_data_raw.csv"
    processed_path = "data/processed/sales_data_clean.csv"
    
    print("Loading data...")
    try:
        df = load_data(raw_path)
        print("Data loaded successfully.")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
