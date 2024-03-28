from helpers.xml_to_csv_helper import convert_xml_to_csv, convert_xml_to_metadata
import os
def convert_xml_to_metadata_task(**context):
    res_path = os.path.join(os.path.dirname(__file__), 'resources')
    run_id = context['dag_run'].run_id
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='extract') 
    return convert_xml_to_metadata(run_id, data)
def convert_xml_to_data_task(**context):
    res_path = os.path.join(os.path.dirname(__file__), 'resources')
    run_id = context['dag_run'].run_id
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='extract') 
    return convert_xml_to_csv(run_id,data)