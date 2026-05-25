import pandas as pd
from sqlalchemy import create_engine

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.db_config import BANKING_DB_URL

engine = create_engine(BANKING_DB_URL)
df = pd.read_sql("SELECT * FROM raw.bank_transactions", engine)

print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nNull Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nSample Data:")
print(df.head())