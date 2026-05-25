from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "somaiah",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="banking_etl_orchestration_pipeline",
    description="Orchestrates banking ETL, staging, analytics, fraud alerts, and KPI summary layers.",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["banking", "data-engineering", "fraud-analytics"],
) as dag:

    extract_excel = BashOperator(
        task_id="extract_excel_preview",
        bash_command="cd /opt/airflow && python scripts/extract_excel.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    load_raw = BashOperator(
        task_id="load_raw_data",
        bash_command="cd /opt/airflow && python scripts/load_raw_data.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    validate_raw = BashOperator(
        task_id="validate_raw_data",
        bash_command="cd /opt/airflow && python scripts/validate_raw_data.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    transform_staging = BashOperator(
        task_id="transform_staging_data",
        bash_command="cd /opt/airflow && python scripts/transform_staging_data.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    create_analytics = BashOperator(
        task_id="create_analytics_layer",
        bash_command="cd /opt/airflow && python scripts/create_analytics_layer.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    create_fraud_alerts = BashOperator(
        task_id="create_fraud_alerts",
        bash_command="cd /opt/airflow && python scripts/create_fraud_alerts.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    create_branch_kpis = BashOperator(
        task_id="create_branch_kpis",
        bash_command="cd /opt/airflow && python scripts/create_branch_kpis.py",
        env={
            "BANKING_DB_URL": "postgresql://admin:admin@host.docker.internal:5432/banking_dw"
        },
    )

    (
        extract_excel
        >> load_raw
        >> validate_raw
        >> transform_staging
        >> create_analytics
        >> create_fraud_alerts
        >> create_branch_kpis
    )