import requests
import streamlit as st
import asyncio
import websockets
from upload_to_s3 import upload_to_s3
from kafka_helper_functions import produce_message
import zipfile
from trigger_dag import trigger_dag
# Endpoint URLs
GET_DAG_STATUS_URL = "http://fastapi-service:8000/dag_status/"
def get_dag_status(dag_run_id):
    response = requests.get(GET_DAG_STATUS_URL + dag_run_id)
    return response.json()

async def receive_updates(dag_run_id):
    uri = f"ws://fastapi-service:8000/ws/{dag_run_id}"  # Replace with your FastAPI server URL
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            st.write("Received update:", message)
def fetch_updates(dag_run_id):
    if dag_run_id:
        st.write(f"Waiting for updates...")
        try:
            asyncio.run(receive_updates(dag_run_id))
            st.write(f"Task Completed")
        except asyncio.exceptions.CancelledError:
            print("WebSocket task was cancelled.")
        except Exception as e:
            st.write(f"Task Completed")
def triggerDag(s3_uri,file_name,dag_id='bigdag'):
        if s3_uri:
            st.success("File uploaded successfully!")
            st.write("S3 URI:", s3_uri)
            dag_run_info, rid = trigger_dag(dag_id, s3_uri=s3_uri)
            run_id = rid
            st.write(dag_run_info)
            dag_run_id = run_id
            fetch_updates(dag_run_id)
def process_pdf(uploaded_file):
    temp_file_path = f"/tmp/{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

        # Upload the file to S3
    s3_uri = upload_to_s3(temp_file_path, object_name=f"t1/{uploaded_file.name}")
    if s3_uri:
        # st.success("File uploaded successfully!")
        # st.write("S3 URI:", s3_uri)
        triggerDag(s3_uri=s3_uri, file_name=uploaded_file.name) 
def process_zip_and_trigger_dag(file_name, zip_ref, dag_id='bigdag'):
    if file_name.endswith('.pdf') and not file_name.startswith('__MACOSX'):
        temp_file_path = f"/tmp/{file_name}"
        st.write(temp_file_path)
        with open(temp_file_path, "wb") as f:
            f.write(zip_ref.read(file_name))
        # Upload the file to S3
        s3_uri = upload_to_s3(temp_file_path, object_name=f"t1/{file_name}")    
        st.write(s3_uri)
        return s3_uri
def process_pdf_files_concurrently(uploaded_zip_file, dag_id='bigdag'):
    with zipfile.ZipFile(uploaded_zip_file, 'r') as zip_ref:
        total_files = len([file_name for file_name in zip_ref.namelist() if file_name.endswith('.pdf')])
        progress_bar = st.progress(0)
        files_processed = 0
        st.write(zip_ref.namelist())
        for file_name in zip_ref.namelist():
            if '/' in file_name:
                files_processed += 1
                progress = files_processed / total_files
                progress_bar.progress(progress)
                continue
            st.write(file_name)
            s3_uri = process_zip_and_trigger_dag(file_name, zip_ref, dag_id)
            produce_message(message=f'{s3_uri}')
            st.write(f"produced message for {s3_uri}")
            files_processed += 1
            progress = files_processed / total_files
            progress_bar.progress(progress)
     