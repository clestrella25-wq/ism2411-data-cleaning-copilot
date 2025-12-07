# ISM2411 - Data Cleaning Project
# Purpose: The prpose is to clean sales data in the csv file handle  missing data and standardizing column names
 
 
import pandas as pd
import os
# I removed the re and unicodedata imports Copilot added because I simplified the code to use Pandas


def load_data(file_path):
    # This is just what loads the CSV file I manually added a check to make sure the file actually exists so the program doesnt crash with a error.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
   
    return pd.read_csv(file_path)


def clean_column_names(df):
    # Copilot originally suggested a complecated function with functions here.
    # I completely rewrote this to be simpler using a Pandas string methods.
    # I want everything lowercase and using underscores
   
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') # This is the simpler version that doesnt use all of the functions that copilot gave in the previous commits.

    # Sometimes datasets could have two columns that could have the same name. This loop checks and prevents that
    seen = {}
    new_columns = []
   
    for col in df.columns:
        if col in seen:
            count = seen[col]
            new_name = f"{col}_v{count}" # I changed this because I specifically wanted v for version
            seen[col] += 1
            new_columns.append(new_name)
        else:
            # If it's new a new column I keep it
            seen[col] = 1
            new_columns.append(col)

    df.columns = new_columns
    return df


def handle_missing_values(df):
    # Copilot tried to use advanced list comprehensions to guess column keywords, but I changed it to a regular loop because gussing wouldbe wrong

    for col in df.columns:
        # check if this is a price column
        if 'price' in col or 'cost' in col:
            # This is to force it to be numbers
            df[col] = pd.to_numeric(df[col], errors='coerce')
           
            # Copilot wanted to use the median.
            # I decided to fill with 0.0 because if a price is missing, I don't want to guess a random number.
            df[col] = df[col].fillna(0.0) # I switched from median() to 0.0 because guessing is wrong.
           
        elif 'quantity' in col or 'qty' in col:
            df[col] = pd.to_numeric(df[col], errors='coerce')
           
            # Copilot wanted to fill missing quantities with 0, but I make it drop the row because without them, the data probably is less useful
            df.dropna(subset=[col], inplace=True) # I switched from fillna(0) to dropping the row

    return df


def remove_invalid_rows(df):
    # Copilot suggested filtering where price >= 0.
    # I changes this to make sure that it was more than 0.
    if 'quantity' in df.columns and 'price' in df.columns:
        df = df[(df['quantity'] > 0) & (df['price'] >= 0)]
    return df


if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())







