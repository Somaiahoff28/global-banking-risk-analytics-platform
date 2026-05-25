import pandas as pd
from sqlalchemy import create_engine
import sys
from pathlib import Path

# PostgreSQL connection
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.db_config import BANKING_DB_URL

engine = create_engine(BANKING_DB_URL)

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