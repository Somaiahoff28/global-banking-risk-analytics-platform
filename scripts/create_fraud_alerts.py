import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://admin:admin@localhost:5432/banking_dw"
)

df = pd.read_sql(
    "SELECT * FROM analytics.fact_transactions",
    engine
)

def classify_fraud_risk(row):
    amount = row.get("transaction_amount", 0)
    balance = row.get("account_balance", 0)
    transaction_type = str(row.get("transaction_type", "")).upper()

    if amount > 10000:
        return "CRITICAL_RISK"
    elif amount > 5000:
        return "HIGH_RISK"
    elif transaction_type == "DEBIT" and balance < 1000:
        return "LOW_BALANCE_DEBIT_RISK"
    else:
        return "NORMAL"

df["fraud_risk_category"] = df.apply(classify_fraud_risk, axis=1)

fraud_alerts = df[df["fraud_risk_category"] != "NORMAL"]

fraud_alerts.to_sql(
    name="fraud_alerts",
    con=engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

print("Fraud alerts table created successfully.")
print(f"Total fraud/risk alerts: {len(fraud_alerts)}")