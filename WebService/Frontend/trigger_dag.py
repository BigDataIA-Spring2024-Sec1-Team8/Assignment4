import streamlit as st
import uuid
import requests
TRIGGER_DAG_URL = "http://fastapi-service:8000/trigger_dag/"

def trigger_dag(dag_id, s3_uri):
    run_id = str(uuid.uuid4())
    dag_run_body = {
        "dag_run_id": run_id,
        "conf": {
            "s3_uri": s3_uri
        }
    }
    response = requests.post(TRIGGER_DAG_URL + dag_id, json=dag_run_body)
    return response.json(), run_id

