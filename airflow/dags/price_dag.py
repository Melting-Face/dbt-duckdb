from datetime import datetime

from constants import (
    execution_config,
    profile_config,
    project_config,
)
from cosmos import DbtTaskGroup

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="price_processing",
    tags=["price"],
    start_date=datetime(2024, 3, 7),
    schedule_interval="@daily",
):
    s = EmptyOperator(task_id="start")

    dbt_task = DbtTaskGroup(
        profile_config=profile_config,
        project_config=project_config,
        operator_args={
            "install_deps": True,
            "should_store_compiled_sql": True,
        },
        execution_config=execution_config,
    )

    e = EmptyOperator(task_id="end")

    s >> dbt_task >> e
