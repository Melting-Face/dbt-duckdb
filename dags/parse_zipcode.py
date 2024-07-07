import time
from datetime import datetime

import duckdb
import requests
from bs4 import BeautifulSoup as bs

from airflow.decorators import dag, task


@dag(
    dag_id="parse_zipcode",
    start_date=datetime(2024, 3, 15),
    catchup=False,
    schedule_interval=None,
)
def parse_zipcode():
    @task
    def get_zipcode():
        conn = duckdb.connect("/opt/airflow/warehouse/dbt.duckdb")
        df = conn.sql(
            "select * from main_silver.center_address where zip_code = ''",
        ).df()
        for index, row in df.iterrows():
            address = row["address"]
            response = requests.get(f"https://juso.app/search?q={address}")
            time.sleep(0.4)
            html = response.text
            html = bs(html, "html.parser")
            links = html.select(".text-center a")
            if len(links) != 1:
                conn.sql(f"""
update main_silver.center_address
set zip_code = '-'
where center_id = {row['center_id']}
                """)
                continue
            href = links[0].get("href")
            print(f"{index} / {df.shape[0]} https://juso.app{href}")
            response = requests.get(f"https://juso.app{href}")
            time.sleep(0.4)
            html = response.text
            html = bs(html, "html.parser")
            infos = html.select(".mt-10 p")
            if len(infos) < 1:
                continue
            zip_code = infos[0].text
            conn.sql(f"""
update main_silver.center_address
set zip_code = '{zip_code}'
where center_id = {row['center_id']}
            """)
            print(row["center_id"], zip_code)
            df.loc[index, "zip_code"] = zip_code

    get_zipcode()


parse_zipcode()
