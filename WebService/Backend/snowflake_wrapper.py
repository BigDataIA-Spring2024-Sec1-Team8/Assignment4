from fastapi import FastAPI
from typing import List
import snowflake.connector
import os
app = FastAPI()

# Snowflake connection parameters
snowflake_config = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': 'CFAInstitute',
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}
def get_data(topic: str = None) -> List[dict]:
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    if topic:
        cursor.execute(f"SELECT Topic, LEARNING_OUTCOMES_SECTION FROM LEARNING_OUTCOMES WHERE topic ILIKE '%{topic}%'")
    else:
        cursor.execute("SELECT Topic, LEARNING_OUTCOMES_SECTION FROM LEARNING_OUTCOMES")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"topic": row[0], "learning_outcomes": row[1]} for row in data]

def get_meta_data() -> List[dict]:
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    cursor.execute("SELECT PDF_NAME, ABSTRACT, title FROM METADATA")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"PDF_NAME": row[0],"title": row[2], "abstract": row[1]} for row in data]