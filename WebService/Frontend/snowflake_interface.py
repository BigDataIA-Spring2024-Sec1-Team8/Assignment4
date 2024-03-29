import requests


backend_url = "http://fastapi-service:8000"

def fetch_data(search_topic):
    # Fetch data from FastAPI backend
    response = requests.get(f"{backend_url}/data?topic={search_topic}")
    data = response.json()
    return data

def fetch_meta_data():
    # Fetch data from FastAPI backend
    response = requests.get(f"{backend_url}/metadata")
    data = response.json()
    return data