import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5432/banking_dw"
)

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