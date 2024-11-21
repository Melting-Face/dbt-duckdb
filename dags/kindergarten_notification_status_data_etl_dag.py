from time import sleep
from typing import List

import pandas as pd
import requests
from pendulum import datetime
from pypika import Query, Table, Tuple

from airflow.decorators import dag, task
from airflow.models import Variable
from duckdb_provider.hooks.duckdb_hook import DuckDBHook


@dag(
    schedule=None,
    start_date=datetime(2024, 9, 20, tz="Asia/Seoul"),
    catchup=False,
    max_active_tasks=1,
    # on_failure_callback=on_failure_callback_slack_webhook,
)
def kindergarten_notification_status_data_etl_dag():
    hook = DuckDBHook.get_hook("duckdb_conn_id")
    table_name = "kn_kindergarten_notification_general_status"
    key = Variable.get("kindergarten_notification_api_key")
    url = Variable.get("kindergarten_notification_api_url")

    @task
    def drop_kindergarten_notification_table_if_exists():
        query = f"drop table if exists kidsnote.{table_name}"
        result = hook.get_first(query)
        print(result)

    @task
    def create_kindergarten_notification_table_if_not_exists():
        query = f"""
        create table if not exists kidsnote.{table_name} (
            key varchar,
            kindercode varchar,
            officeedu varchar,
            subofficeedu varchar,
            kindername varchar,
            establish varchar,
            edate varchar,
            odate varchar,
            addr varchar,
            telno varchar,
            faxno varchar,
            hpaddr varchar,
            opertime varchar,
            clcnt3 varchar,
            clcnt4 varchar,
            clcnt5 varchar,
            mixclcnt varchar,
            shclcnt varchar,
            ppcnt3 varchar,
            ppcnt4 varchar,
            ppcnt5 varchar,
            mixppcnt varchar,
            shppcnt varchar,
            rppnname varchar,
            ldgrname varchar,
            pbnttmng varchar,
            prmstfcnt varchar,
            ag3fpcnt varchar,
            ag4fpcnt varchar,
            ag5fpcnt varchar,
            mixfpcnt varchar,
            spcnfpcnt varchar,
            state_code integer,
            city_code integer
        )
        """
        result = hook.get_first(query)
        print(result)

    @task
    def get_kindergarten_notification_address_code() -> List[List[int]]:
        table = Table("kidsnote.common_kindergarten_notification_address_code")
        query = (
            Query.from_(table)
            .select(table.state_code, table.city_code)
            .get_sql(quote_char=None)
        )
        result = hook.get_records(query)
        print(result)
        return result

    @task
    def get_df_from_kindergarten_notification_api(
        address_code: List[int],
    ) -> pd.DataFrame:
        state_code, city_code = address_code
        print(state_code, city_code)
        params = {
            "key": key,
            "sidoCode": state_code,
            "sggCode": city_code,
            "pageCnt": 1000,
            "currentPage": 1,
        }
        response = requests.get(
            url=url,
            params=params,
            verify=False,
        )
        json = response.json()
        print(json)
        sleep(0.5)
        df = pd.DataFrame(json["kinderInfo"])

        if not df.empty:
            df[["state_code", "city_code"]] = state_code, city_code
            df = df.fillna("")

        return df

    @task
    def insert_df_into_rabbit(df: pd.DataFrame):
        if df.empty:
            return

        columns = list(df.columns)
        rows = df.to_numpy().tolist()
        rows = [Tuple(*row).get_sql(quote_char=None) for row in rows]
        query = f"""
        insert into kidsnote.{table_name} ({','.join(columns)})
        values {','.join(rows)}
        """

        result = hook.get_first(query)
        print(result)

    drop_table = drop_kindergarten_notification_table_if_exists()
    create_table = create_kindergarten_notification_table_if_not_exists()
    address_codes = get_kindergarten_notification_address_code()
    dfs = get_df_from_kindergarten_notification_api.expand(address_code=address_codes)
    insert_df_into_rabbit.expand(df=dfs)

    drop_table >> create_table
    create_table >> address_codes


kindergarten_notification_status_data_etl_dag()
