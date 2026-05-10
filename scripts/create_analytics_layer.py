import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql://admin:admin@localhost:5432/banking_dw"
)

# Read staging data
df = pd.read_sql(
    "SELECT * FROM staging.stg_bank_transactions",
    engine
)

print("Staging Data Shape:")
print(df.shape)

# Create transaction risk category
if 'transaction_amount' in df.columns:

    df['risk_category'] = df['transaction_amount'].apply(
        lambda x: (
            'HIGH_RISK'
            if x > 5000
            else 'NORMAL'
        )
    )

# Create analytics table
df.to_sql(
    name="fact_transactions",
    con=engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

print("\nAnalytics fact table created successfully.")
print(f"Rows Loaded: {len(df)}")