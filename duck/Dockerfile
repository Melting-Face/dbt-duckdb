FROM python:3.10-slim

WORKDIR /home/streamlit

ENV HOME=/home/streamlit

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
