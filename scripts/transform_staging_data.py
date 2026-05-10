import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql://admin:admin@localhost:5432/banking_dw"
)

# Read raw table
df = pd.read_sql(
    "SELECT * FROM raw.bank_transactions",
    engine
)

print("Original Shape:")
print(df.shape)

# Standardize column names
df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
)

# Remove duplicate rows
df = df.drop_duplicates()

# Standardize currency column
if 'currency' in df.columns:
    df['currency'] = df['currency'].str.upper()

# Convert transaction amount to numeric
if 'transaction_amount' in df.columns:
    df['transaction_amount'] = pd.to_numeric(
        df['transaction_amount'],
        errors='coerce'
    )

print("\nCleaned Shape:")
print(df.shape)

# Load into staging schema
df.to_sql(
    name="stg_bank_transactions",
    con=engine,
    schema="staging",
    if_exists="replace",
    index=False
)

print("\nStaging table created successfully.")