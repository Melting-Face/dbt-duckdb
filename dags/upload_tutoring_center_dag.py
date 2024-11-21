import math
from time import sleep
import pandas as pd
import requests
from duckdb_provider.hooks.duckdb_hook import DuckDBHook
from pendulum import datetime

from airflow.models import Variable
from airflow.decorators import dag, task
from constants import tutoring_center_codes


@dag(
    schedule=None,
    start_date=datetime(2024, 9, 7, tz="UTC"),
    catchup=False,
    max_active_tasks=3,
)
def upload_tutoring_center_dag():
    hook = DuckDBHook.get_hook("duckdb_conn_id")
    table_name = "kn_centers_tutoring_center"
# KEY = Variable.get("tutoring_center_api_key")
# url = Variable.get("tutoring_center_api_url")
    @task
    def drop_tutoring_center_table_if_exists():
        query = f"drop table if exists {table_name}"
        result = hook.get_first(query)
        print(result)

    @task
    def create_tutoring_center_table_if_not_exists():
        query = f"""
        create table if not exists {table_name} (
            atpt_ofcdc_sc_code varchar,
            atpt_ofcdc_sc_nm varchar,
            admst_zone_nm varchar,
            aca_insti_sc_nm varchar,
            aca_asnum varchar,
            aca_nm varchar,
            estbl_ymd varchar,
            reg_ymd varchar,
            reg_sttus_nm varchar,
            caa_begin_ymd varchar,
            caa_end_ymd varchar,
            tofor_smtot bigint,
            dtm_rcptn_ablty_nmpr_smtot bigint,
            realm_sc_nm varchar,
            le_ord_nm varchar,
            le_crse_list_nm varchar,
            le_crse_nm varchar,
            psnby_thcc_cntnt varchar,
            thcc_othbc_yn varchar,
            brhs_aca_yn varchar,
            fa_rdnma varchar,
            fa_rdnda varchar,
            fa_rdnzc varchar,
            fa_telno varchar,
            load_dtm varchar
        )
        """
        result = hook.get_first(query)
        print(result)


    # @task
    # def get_indexes(tutoring_center_code: str) -> int:
    #     params = {
    #         "KEY": KEY,
    #         "Type": "json",
    #         "pIndex": 1,
    #         "pSize": 1,
    #         "ATPT_OFCDC_SC_CODE": tutoring_center_code,
    #     }
    #     response = requests.get(
    #         url=url,
    #         params=params,
    #     )
    #     json = response.json()
    #     sleep(0.5)
    #     list_total_count = json["acaInsTiInfo"][0]["head"][0]["list_total_count"]
    #     total_index = math.ceil(list_total_count / 1000)
    #     return list(range(1, total_index + 1))


    drop_table = drop_tutoring_center_table_if_exists()
    create_table = create_tutoring_center_table_if_not_exists()


    drop_table >> create_table


    # codes = get_tutoring_center_code()
    # get_df.expand(code=codes)


upload_tutoring_center_dag()
