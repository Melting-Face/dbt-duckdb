from datetime import datetime

from airflow.utils.trigger_rule import TriggerRule

from configs import (
    dbt_executable_path,
    execution_config,
    profile_config,
    project_config,
    project_dir,
)
from cosmos import (
    DbtRunLocalOperator,
    DbtTaskGroup,
    RenderConfig,
)

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="kidsnote_book",
    tags=["price"],
    start_date=datetime(2024, 3, 15),
    catchup=False,
    schedule_interval=None,
):
    start = EmptyOperator(task_id="start")

    dbt_silver_task = DbtRunLocalOperator(
        task_id="dbt_silver_task",
        project_dir=project_dir,
        install_deps=True,
        should_store_compiled_sql=True,
        profile_config=profile_config,
        dbt_executable_path=dbt_executable_path,
        select="kidsnote_book",
    )

    end = EmptyOperator(task_id="end")

    start >> dbt_silver_task >> end
