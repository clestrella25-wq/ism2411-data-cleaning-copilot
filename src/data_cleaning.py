# ISM2411 - Data Cleaning Project
# Purpose: The prpose is to clean sales data in the csv file handle  missing data and standardizing column names
 
import pandas as pd
import os
import re
import unicodedata

def load_data(file_path):
    """
    Loads data from a CSV file.
    """
    # Check if file exists before loading
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
    
    return pd.read_csv(file_path)


def clean_column_names(df):
    """
    Standardize column names to snake_case and remove spaces, punctuation, and accents.

    Rules applied:
    - Convert to string and lowercase
    - Remove accents/diacritics
    - Remove punctuation (keep letters, numbers, and underscore)
    - Replace spaces and hyphens with single underscores
    - Collapse multiple underscores and strip leading/trailing underscores
    - Ensure resulting names are unique by appending numeric suffixes for duplicates

    The function renames columns in-place and returns the same DataFrame.
    """
    def _to_snake(name):
        if not isinstance(name, str):
            name = str(name)
        # Normalize unicode and drop accents
        name = unicodedata.normalize("NFKD", name)
        name = name.encode("ascii", "ignore").decode("ascii")
        name = name.lower()
        # Remove characters that are not word chars, spaces or hyphens
        name = re.sub(r"[^\w\s-]", "", name)
        # Replace spaces and hyphens with underscore
        name = re.sub(r"[\s-]+", "_", name)
        # Collapse multiple underscores
        name = re.sub(r"_+", "_", name)
        # Strip leading/trailing underscores
        name = name.strip("_")
        if name == "":
            name = "unknown_column" # I chnaged this line so i wouldnt get it confused with the other varibles 
        return name

    # Convert all column names
    new_cols = [_to_snake(c) for c in df.columns]

    # Ensure uniqueness
    seen = {}
    unique_cols = []
    for col in new_cols:
        if col in seen:
            cnt = seen[col]
            candidate = f"{col}_v{cnt}"# i put the v so that i can tell which one was the version  
    
            # bump counter until unique
            while candidate in seen:
                cnt += 1
                candidate = f"{col}_{cnt}"
            seen[col] = cnt + 1
            seen[candidate] = 1
            unique_cols.append(candidate)
        else:
            seen[col] = 1
            unique_cols.append(col)

    df.columns = unique_cols
    return df


def handle_missing_values(df):
    """
    Detect and handle missing values in price and quantity-like columns.

    Behavior:
    - Detects columns likely to represent prices (contains 'price', 'amount', 'cost', 'total')
      and quantities (contains 'quantity', 'qty', 'units', 'unit'). Matching is case-insensitive
      and expects cleaned column names (snake_case) but will work with raw names too.
    - Coerces those columns to numeric (invalid parsing becomes NaN).
    - For price-like columns: fills NaN with the column median (or 0.0 if median is NaN).
    - For quantity-like columns: fills NaN with 0.

    The function mutates `df` in-place and returns it.
    """
    cols = list(df.columns)
    lower_cols = [c.lower() for c in cols]

    price_keywords = ("price", "amount", "cost", "total")
    qty_keywords = ("quantity", "qty", "units", "unit")

    price_cols = [cols[i] for i, c in enumerate(lower_cols) if any(k in c for k in price_keywords)]
    qty_cols = [cols[i] for i, c in enumerate(lower_cols) if any(k in c for k in qty_keywords)]

    # Coerce and impute price columns
    for col in price_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
       # I took off the median logic because guessing prices is not correct
        df[col].fillna(0.0, inplace=True) # I changed this and changed the missing price with 0 instead of wiht the median

    # Coerce and impute quantity columns
    for col in qty_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
       # I took off the fillna(0) logic because a sale with 0 items isnt valid
        df.dropna(subset=[col], inplace=True) # I changed this so I dropped rows that had missing quantity instead of filling them with 0


    return df

if __name__ == "__main__":
    # Define paths
    raw_path = "data/raw/sales_data_raw.csv"
    processed_path = "data/processed/sales_data_clean.csv"
    
    print("Loading data...")
    try:
        df = load_data(raw_path)
        print("Data loaded successfully.")
        # Clean and show column names
        df = clean_column_names(df)
        print("Cleaned columns:", df.columns.tolist())
        # Show missing counts before handling
        print("Missing counts before handling:\n", df.isna().sum())

        # Handle missing values for price/quantity columns
        df = handle_missing_values(df)
        print("Missing counts after handling:\n", df.isna().sum())
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
