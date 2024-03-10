from datetime import datetime

from constants import execution_config, profile_config, project_config
from cosmos import DbtDag, DbtRunOperationOperator

from airflow.operators.empty import EmptyOperator

with DbtDag(
    project_config=project_config,
    profile_config=profile_config,
    execution_config=execution_config,
    dag_id="price_processing",
    operator_args={
        "install_deps": True,
        "full_refresh": True,
    },
    tags=["price"],
    start_date=datetime(2024, 3, 7),
    schedule_interval="@daily",
):
    dbt_stage_external_sources = DbtRunOperationOperator(
        task_id="stage_external_sources",
        dag_id="price_processing",
        macro_name="stage_external_sources",
    )

    s = EmptyOperator(task_id="start")
    e = EmptyOperator(task_id="end")

    s >> dbt_stage_external_sources >> e
