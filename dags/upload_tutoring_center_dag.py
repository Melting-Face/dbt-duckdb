import pandas as pd
from duckdb_provider.hooks.duckdb_hook import DuckDBHook
from pendulum import datetime

from airflow.decorators import dag, task

hook = DuckDBHook.get_hook("duckdb_conn_id")


@dag(
    schedule=None,
    start_date=datetime(2024, 9, 7, tz="UTC"),
    catchup=False,
)
def upload_tutoring_center_dag():
    @task
    def get_tutoring_center_code():
        conn = hook.get_conn()
        sql = """
select
    code
from common_tutoring_center_code
        """
        df: pd.Dataframe = conn.execute(sql).df()
        return df.to_numpy().tolist()

    codes = get_tutoring_center_code()

upload_tutoring_center_dag()
