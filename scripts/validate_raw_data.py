import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://admin:admin@localhost:5432/banking_dw")

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