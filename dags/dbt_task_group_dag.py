from configs import (
    execution_config,
    profile_config,
    project_config,
)
from cosmos import DbtTaskGroup, RenderConfig
from pendulum import datetime

from airflow.decorators import dag


@dag(schedule=None, start_date=datetime(2024, 7, 27), catchup=False)
def dbt_task_group_dag():
    silver = DbtTaskGroup(
        group_id="silver",
        project_config=project_config,
        render_config=RenderConfig(
            select=["forecast_zone_information"],
        ),
        execution_config=execution_config,
        operator_args={"install_deps": True},
        profile_config=profile_config,
    )

    silver

dbt_task_group_dag()
