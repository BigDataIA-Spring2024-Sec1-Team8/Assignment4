from pydantic import BaseModel, Field, validator
import pandas as pd
import os
class LearningOutcomes(BaseModel):
    topic: str = Field(..., alias='topic', min_length=2)  
    outcomes: str = Field(default="Not defined", min_length=2)

    @validator('topic', 'outcomes', pre=True, each_item=False)
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            ValueError('empty not allowed')
        return v
class MetaData(BaseModel):
    title: str = Field(alias='Title', default="Unknown")  
    publisher: str = Field(default="Unknown")
    availability_status: str = Field(default="", alias='availability_status')
    analytic: str = Field(default="Not Available", alias='analytic', min_length=2)
    imprinted_date: str = Field(..., alias='imprinted_date')  
    abstract: str = Field(default="", min_length=2)

    @validator('title', 'publisher', 'availability_status', 'analytic', 'imprinted_date', 'abstract', pre=True, each_item=False)
    def check_empty_string(cls, v,values):
        if v == "":
            raise ValueError(f'empty string not allowed')

        return v
def validate_data(run_id, csv_filename):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')  # Create a folder named 'downloaded_files' in the DAG folder
    res_path = os.path.join(res_path, str(run_id))

    c1 = os.path.join(res_path,csv_filename)
    df = pd.read_csv(c1)
    try:
        for _, row in df.iterrows():
            instance = LearningOutcomes(
                    topic=row['Topic'], 
                    outcomes=row['Learning_Outcomes_Section']
            )
    except Exception as e:
        print(str(e))
    return csv_filename
def validate_metadata(run_id, csv_filename):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    res_path = os.path.join(res_path, str(run_id))
    c1 = os.path.join(res_path,csv_filename)
    df = pd.read_csv(c1)
    try:
        for _, row in df.iterrows():
            instance = MetaData(
                    title=row['Title'], 
                    publisher=row['Publisher'],
                    availability_status=row['AvailabilityStatus'],
                    analytic = row['Analytic'],
                    imprinted_date = row['ImprintedDate'],
                    abstract = row['Abstract'] 
            )
    except Exception as e:
        print(str(e))
    return csv_filename