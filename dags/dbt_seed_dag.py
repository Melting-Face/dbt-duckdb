from datetime import datetime

from configs import (
    dbt_executable_path,
    profile_config,
    project_dir,
)
from cosmos.operators import DbtDocsS3Operator, DbtSeedOperator

from airflow.decorators import dag


@dag(
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    tags=["dbt", "seed"],
    catchup=False,
)
def dbt_seed_dag():
    seed = DbtSeedOperator(
        task_id="seed_dbt_dip",
        project_dir=project_dir,
        profile_config=profile_config,
        dbt_executable_path=dbt_executable_path,
        install_deps=False,
    )

    generate_dbt_docs_s3 = DbtDocsS3Operator(
        task_id="generate_dbt_docs_s3",
        bucket_name="warehouse",
        connection_id="s3_conn_id",
        dbt_executable_path=dbt_executable_path,
        project_dir=project_dir,
        profile_config=profile_config,
    )

    seed >> generate_dbt_docs_s3


dbt_seed_dag()
