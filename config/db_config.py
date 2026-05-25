import os

BANKING_DB_URL = os.getenv(
    "BANKING_DB_URL",
    "postgresql://admin:admin@localhost:5432/banking_dw"
)