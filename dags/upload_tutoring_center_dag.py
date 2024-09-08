import pandas as pd
import requests
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
        df = conn.execute(sql).df()
        return df.to_numpy().flatten().tolist()

    @task
    def get_df(code):
        url = "https://open.neis.go.kr/hub/acaInsTiInfo"
        params = {
            "KEY": "6f05968fce924b00aa9253e3e95f3bf9",
            "Type": "json",
            "pIndex": 1,
            "pSize": 1000,
            "ATPT_OFCDC_SC_CODE": code,
        }
        raw_response = requests.get(
            url,
            params=params,
        )
        response = raw_response.json()["acaInsTiInfo"]["row"]
        df = pd.DataFrame(response)
        return df

    codes = get_tutoring_center_code()
    get_df.expand(code=codes)


upload_tutoring_center_dag()
