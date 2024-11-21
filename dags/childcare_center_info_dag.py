from io import StringIO
from time import sleep

import pandas as pd
import requests
from constants import childcare_open_api_arnames
from pendulum import datetime

from airflow.decorators import dag, task
from airflow.models import Variable



@dag(
    schedule_interval=None,
    start_date=datetime(2024, 10, 3, tz="Asia/Seoul"),
    catchup=False,
    max_active_tasks=3,
    # on_failure_callback=on_failure_callback_slack_webhook,
)
def childcare_center_info_dag():
    state_city_api_key = Variable.get("state_city_api_key")
    state_city_api_url = Variable.get("state_city_api_url")

    @task
    def get_arcodes_from_api(arname: str):
        params = {
            "key": state_city_api_key,
            "arname": arname,
        }
        response = requests.get(
            url=state_city_api_url,
            params=params,
        )
        sleep(0.5)
        df = pd.read_xml(StringIO(response.text))
        df = df.loc[:, ["arcode"]]
        return df.to_numpy().flatten().tolist()

    for arname in childcare_open_api_arnames:
        arcodes = get_arcodes_from_api(arname)


childcare_center_info_dag()
