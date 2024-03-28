from helpers.validate_with_pydantic_helper import validate_data, validate_metadata
def validate_data_task(**context):
    print(context)
    task_instance = context['task_instance']
    run_id = context['dag_run'].run_id
    data = task_instance.xcom_pull(task_ids='convert_xml_to_data_task')    
    return validate_data(run_id,data)
def validate_meta_data_task(**context):
    print(context)
    task_instance = context['task_instance']
    run_id = context['dag_run'].run_id
    data = task_instance.xcom_pull(task_ids='convert_xml_to_metadata_task')    
    return validate_metadata(run_id, data)