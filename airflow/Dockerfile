FROM apache/airflow:2.9.3-python3.10

WORKDIR /opt/airflow

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt
