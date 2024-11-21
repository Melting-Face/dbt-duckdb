# from io import BytesIO
#
# import pandas as pd
# import requests
# from pendulum import datetime
#
# from airflow.decorators import dag, task
# from airflow.models import Variable
# from airflow.providers.amazon.aws.hooks.s3 import S3Hook
#
# s3_hook = S3Hook(aws_conn_id="s3_conn_id")
#
#
# @dag(schedule=None, start_date=datetime(2024, 7, 27), catchup=False)
# def weather_data_api_dag():
#     @task
#     def request_forecast_zone_information():
#         service_key = Variable.get("open_data_service_key")
#         service_url = Variable.get("forecast_zone_information_service_url")
#         params = {
#             "serviceKey": service_key,
#             "pageNo": "1",
#             "numOfRows": "10000",
#             "dataType": "JSON",
#         }
#         raw_response = requests.get(
#             service_url,
#             params=params,
#         )
#
#         response = raw_response.json()["response"]
#         assert response["header"]["resultCode"] == "00"
#         return response["body"]["items"]["item"]
#
#     @task
#     def get_df_from_response(items):
#         df = pd.DataFrame(items)
#         return df
#
#     @task
#     def upload_df_to_s3(df: pd.DataFrame):
#         bytesio = BytesIO()
#         df.to_parquet(bytesio, index=False, compression="gzip")
#         bytesio.seek(0)
#         s3_hook.load_bytes(
#             bytes_data=bytesio.getvalue(),
#             bucket_name="warehouse",
#             key="dbt/forecast_zone_information.parquet.gzip",
#             replace=True,
#         )
#
#     items = request_forecast_zone_information()
#     df = get_df_from_response(items)
#     upload_df_to_s3(df)
#
#
# weather_data_api_dag()
