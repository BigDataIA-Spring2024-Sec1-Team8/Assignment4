import pandas as pd
import snowflake.connector
import os
def upload_data_to_snowflake(run_id,csv_filename):

    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_user =  os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_warehouse =os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        schema=snowflake_schema
    )

    cursor = conn.cursor()

    target_database = 'CFAInstitute'
    target_table = 'Learning_Outcomes'

    create_database_query = f"CREATE DATABASE IF NOT EXISTS {target_database}"
    cursor.execute(create_database_query)

    use_database_query = f"USE DATABASE {target_database}"
    cursor.execute(use_database_query)
    cursor.execute("USE WAREHOUSE BIGDATA")

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {target_table} (
        Topic VARCHAR,
        Learning_Outcomes_Section VARCHAR
    )
    """

    cursor.execute(create_table_query)
    cursor.execute(f"TRUNCATE TABLE {target_table}")
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')  # Create a folder named 'downloaded_files' in the DAG folder
    res_path = os.path.join(res_path, str(run_id))
    # csv_filename='l1.csv'
    c1 = os.path.join(res_path,csv_filename)
    print(c1)
    cursor.execute(f"PUT file://{c1} @%{target_table}")

    cursor.execute(f"COPY INTO {target_table} ON_ERROR=CONTINUE FILE_FORMAT = (FIELD_OPTIONALLY_ENCLOSED_BY = '\"' SKIP_HEADER=1 PARSE_HEADER = FALSE)")

def upload_metadata_to_snowflake(run_id,csv_filename):

    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_user =  os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_warehouse =os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        schema=snowflake_schema
    )

    cursor = conn.cursor()

    target_database = 'CFAInstitute'
    target_table = 'Metadata'

    create_database_query = f"CREATE DATABASE IF NOT EXISTS {target_database}"
    cursor.execute(create_database_query)

    use_database_query = f"USE DATABASE {target_database}"
    cursor.execute(use_database_query)
    cursor.execute("USE WAREHOUSE BIGDATA")

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {target_table} (
        PDF_NAME String,
        Title String,
        Publisher String,
        AvailabilityStatus String,
        Analytic String,
        ImprintedDate String,
        AppInfoDescription String,
        Abstract String
    )
    """

    cursor.execute(create_table_query)
    cursor.execute(f"TRUNCATE TABLE {target_table}")

    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources') # Create a folder named 'downloaded_files' in the DAG folder
    # csv_filename='l1.csv'
    res_path = os.path.join(res_path, str(run_id))
    c1 = os.path.join(res_path,csv_filename)
    print(c1)
    cursor.execute(f"PUT file://{c1} @%{target_table}")

    cursor.execute(f"COPY INTO {target_table} ON_ERROR=CONTINUE FILE_FORMAT = (FIELD_OPTIONALLY_ENCLOSED_BY = '\"' SKIP_HEADER=1 PARSE_HEADER = FALSE)")