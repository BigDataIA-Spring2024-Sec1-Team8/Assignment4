from grobid_client.grobid_client import GrobidClient
import os
def extract(**context):
    config_filename = "config.json"
    local_path = "./"
    os.makedirs(local_path, exist_ok=True)
    local_path = os.path.join(os.path.dirname(__file__), 'config')
    config = os.path.join(local_path, config_filename)
    client = GrobidClient(config_path=config)
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    run_id = context['dag_run'].run_id
    res_path = os.path.join(res_path, str(run_id))
    print(res_path)
    client.process("processFulltextDocument", res_path, output=res_path, consolidate_citations=True, tei_coordinates=True, force=True)
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='download_from_s3')  
    print(data)  
    return data.replace('pdf','grobid.tei.xml')
