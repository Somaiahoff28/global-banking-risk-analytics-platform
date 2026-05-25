import pandas as pd
from sqlalchemy import create_engine

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.db_config import BANKING_DB_URL

engine = create_engine(BANKING_DB_URL)
df = pd.read_excel("data/banking_dataset.xlsx")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df.to_sql(
    "bank_transactions",
    engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print("Raw data loaded successfully into PostgreSQL.")
print(f"Rows loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")