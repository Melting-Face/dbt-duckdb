from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="price_processing",
    tags=["price"],
    start_date=datetime(2024, 3, 15),
    catchup=False,
    # schedule_interval="none",
):
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

    s = EmptyOperator(task_id="start")

    dbt_silver_price_task_group = DbtTaskGroup(
        group_id="dbt_silver_price_task_group",
        profile_config=profile_config,
        project_config=project_config,
        operator_args={
            "install_deps": True,
            "should_store_compiled_sql": True,
        },
        render_config=RenderConfig(
            select=["tag:silver,tag:price"],
            exclude=["tag:union"],
        ),
        execution_config=execution_config,
    )

    dbt_silver_price_union_task = DbtRunLocalOperator(
        task_id="dbt_silver_price_union_task",
        project_dir=project_dir,
        install_deps=True,
        should_store_compiled_sql=True,
        profile_config=profile_config,
        dbt_executable_path=dbt_executable_path,
        select="tag:silver,tag:price,tag:union",
    )

    e = EmptyOperator(task_id="end")

    s >> dbt_silver_price_task_group >> dbt_silver_price_union_task >> e
