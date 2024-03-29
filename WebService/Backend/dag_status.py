import requests
import asyncio
AIRFLOW_API_BASE_URL = "http://test-airflow-1269873075.us-east-2.elb.amazonaws.com/api/v1"
# AIRFLOW_API_BASE_URL = "http://host.docker.internal:8080/api/v1"

async def fetch_dag_status(dag_run_id):
    AUTHORIZATION_HEADER = "Basic YWlyZmxvdzphaXJmbG93"
    response = requests.get(f"{AIRFLOW_API_BASE_URL}/dags/bigdag/dagRuns/{dag_run_id}", headers={
        "Authorization": AUTHORIZATION_HEADER,
        "Content-Type": 'application/json'
    })
    response.raise_for_status()
    res = response.json()
    dag_run_state = res["state"]
    end_date = res['end_date']
    return dag_run_state, end_date

async def send_dag_status(websocket, dag_run_id, active_connections):
    while dag_run_id in active_connections:
        try:
            dag_run_state, end_date = await fetch_dag_status(dag_run_id)
            await websocket.send_json({"dag_run_id": dag_run_id, "status": dag_run_state, "end_date": end_date})
            
            # If DAG run state is "success", send completion message and close connection
            if dag_run_state == "success" or dag_run_state == 'failed':
                await websocket.send_text("DAG run completed.")
                await websocket.close()
                if dag_run_id in active_connections:
                    del active_connections[dag_run_id]  # Remove connection from active_connections
                return
            
        except Exception as e:
            await websocket.send_json({"error": str(e)})
        
        await asyncio.sleep(5)  # Fetch status every 5 seconds
