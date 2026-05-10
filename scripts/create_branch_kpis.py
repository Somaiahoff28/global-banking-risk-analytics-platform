import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://admin:admin@localhost:5432/banking_dw"
)

df = pd.read_sql(
    "SELECT * FROM analytics.fact_transactions",
    engine
)

branch_kpis = df.groupby("branch").agg(
    total_transactions=("transaction_amount", "count"),
    total_transaction_amount=("transaction_amount", "sum"),
    average_transaction_amount=("transaction_amount", "mean"),
    total_account_balance=("account_balance", "sum")
).reset_index()

branch_kpis.to_sql(
    name="branch_kpi_summary",
    con=engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

print("Branch KPI summary table created successfully.")
print(f"Branches summarized: {len(branch_kpis)}")