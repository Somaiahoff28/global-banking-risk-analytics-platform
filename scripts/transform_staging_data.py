import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.db_config import BANKING_DB_URL

engine = create_engine(BANKING_DB_URL)

df = pd.read_sql(
    "SELECT * FROM raw.bank_transactions",
    engine
)

print("Original Shape:")
print(df.shape)

df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
)

df = df.drop_duplicates()

if "currency" in df.columns:
    df["currency"] = df["currency"].astype(str).str.upper()

if "transaction_amount" in df.columns:
    df["transaction_amount"] = pd.to_numeric(
        df["transaction_amount"],
        errors="coerce"
    )

if "account_balance" in df.columns:
    df["account_balance"] = pd.to_numeric(
        df["account_balance"],
        errors="coerce"
    )

print("\nCleaned Shape:")
print(df.shape)

df.to_sql(
    name="stg_bank_transactions",
    con=engine,
    schema="staging",
    if_exists="replace",
    index=False
)

print("\nStaging table created successfully.")