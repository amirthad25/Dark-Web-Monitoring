import pandas as pd

# Load datasets
credentials_file = "leaked_credentials.csv"
breach_file = "data_breach.csv"

# Load leaked credentials dataset
credentials_df = pd.read_csv(credentials_file)
breaches_df = pd.read_csv(breach_file, delimiter=";")

# 1️⃣ Clean leaked_credentials.csv
credentials_df = credentials_df.drop_duplicates()  # Remove duplicates
credentials_df = credentials_df.dropna()  # Remove empty rows

# Standardize phone numbers (remove spaces & special chars)
credentials_df["phone_number"] = credentials_df["phone_number"].str.replace(r'\D', '', regex=True)

# Convert all text to lowercase (case-insensitive matching)
credentials_df["email"] = credentials_df["email"].str.lower()
credentials_df["password"] = credentials_df["password"].astype(str).str.lower()

# 2️⃣ Clean data_breach.csv
breaches_df = breaches_df.drop_duplicates()
breaches_df = breaches_df.dropna(subset=["Entity", "Records Lost", "Method of Leak"])  # Remove rows missing key info

# Fix the "Records Lost" column: Remove commas & convert to integer
def clean_records_lost(value):
    if isinstance(value, str):
        value = value.replace(',', '').strip()  # Remove commas
        try:
            return int(float(value))  # Convert to integer
        except ValueError:
            return None  # Set to None if conversion fails
    return value  # Return original if already numeric

breaches_df["Records Lost"] = breaches_df["Records Lost"].apply(clean_records_lost)

# Standardize column names (remove spaces)
breaches_df.columns = breaches_df.columns.str.strip()

# Save the cleaned datasets
credentials_df.to_csv("cleaned_credentials.csv", index=False)
breaches_df.to_csv("cleaned_breaches.csv", index=False)

print("✅ Data cleaning complete. Files saved as 'cleaned_credentials.csv' and 'cleaned_breaches.csv'.")
