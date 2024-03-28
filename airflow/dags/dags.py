from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
from tasks.download_from_s3 import download_from_s3
from tasks.extract_task import extract
from tasks.convert_to_csv import convert_xml_to_data_task, convert_xml_to_metadata_task
from tasks.validate_tasks import validate_data_task, validate_meta_data_task
from tasks.upload_data_task import upload_data_to_snowflake_task, upload_metadata_data_to_snowflake_task
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'bigdag',
    default_args=default_args,
    description='Download PDF file from S3',
    start_date=datetime(2024, 3, 19),
    schedule_interval=None,
    catchup=False
)


def remove_files_task(**context):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    run_id = context['dag_run'].run_id
    res_path = os.path.join(res_path, str(run_id))

    for filename in os.listdir(res_path):
        file_path = os.path.join(res_path, filename)
        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)
    os.rmdir(res_path)
task_download_from_s3 = PythonOperator(
        task_id='download_from_s3',
        python_callable=download_from_s3,
        dag=dag
    )
extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        dag=dag
    )
xml_conversion_data_task = PythonOperator(
        task_id='convert_xml_to_data_task',
        python_callable=convert_xml_to_data_task,
        dag=dag
    )
xml_conversion_metadata_task = PythonOperator(
        task_id='convert_xml_to_metadata_task',
        python_callable=convert_xml_to_metadata_task,
        dag=dag
    )
validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data_task,
        dag=dag
    )
validate_metadata_task = PythonOperator(
        task_id='validate_meta_data',
        python_callable=validate_meta_data_task,
        dag=dag
    )
upload_data_task = PythonOperator(
        task_id='upload_data_to_snowflake_task',
        python_callable=upload_data_to_snowflake_task,
        dag=dag
    )
upload_meta_task = PythonOperator(
        task_id='upload_metadata_data_to_snowflake_task',
        python_callable=upload_metadata_data_to_snowflake_task,
        dag=dag
    )
clean_task = PythonOperator(
        task_id='clean_task',
        python_callable=remove_files_task,
        dag=dag
    )
task_download_from_s3 >> extract_task

extract_task >> [xml_conversion_data_task, xml_conversion_metadata_task]

xml_conversion_data_task>> validate_task >> upload_data_task

xml_conversion_metadata_task>> validate_metadata_task >> upload_meta_task

[upload_data_task,upload_meta_task] >> clean_task