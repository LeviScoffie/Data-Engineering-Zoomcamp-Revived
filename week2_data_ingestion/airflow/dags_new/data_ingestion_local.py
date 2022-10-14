import os
import logging
import pandas as pd
from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from ingest_script import ingest_callable


import pyarrow.csv as pv # convert dataset into parquet before converted to gcs. but not needed since already in parquet.
import pyarrow.parquet as pq
# Create A DAG 
# airflow home is an environmental variable. We save the date to airflow home becasue when we save it to the default location /temp ..
# all files will be removed after task finshed
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME","/opt/AIRFLOW/")


PG_HOST=os.getenv("PG_HOST")
PG_USER=os.getenv("PG_USER")
PG_PASSWORD=os.getenv("PG_PASSWORD")
PG_PORT=os.getenv("PG_PORT")
PG_DATABASE=os.getenv("PG_DATABASE")


local_workflow= DAG(
    "LocalIngestionDAG",
    # parameterize the DAG by month
    schedule_interval="0 7 2 * *",
    start_date=datetime(2021, 1, 1)
)

#parameterizing becasue of the dags running in parralel of months data being downloaded.

URL_PREFIX= 'https://d37ci6vzurychx.cloudfront.net/trip-data'
URL_TEMPLATE =URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
OUTPUT_FILE_TEMPLATE= AIRFLOW_HOME +'/output_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
CSV_FILE_INPUT=OUTPUT_FILE_TEMPLATE.replace('.parquet','.csv')
TABLE_NAME_TEMPLATE ='yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'


def format_to_csv (src_file):
    if not src_file.endswith('.parquet'):
        logging.error("Can only accept source files in parquet format, for the moment")
        return
    
    df= pd.read_parquet(src_file)
    csv_name=src_file.replace('.parquet','.csv')
    df=df.to_csv(csv_name, index=False)
    # pv.write_csv(table, src_file.replace('.parquet','.csv'))
    
    
with local_workflow: # creating of tasks. 1. wget to download 2. format to csv 3. ingest
    
    

    wget_task = BashOperator(
        
        task_id='wget_data_download',
        
        ## the L in sSL is used for redirecting to actual site where the content is located.
        
        bash_command=f"curl  -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}"
       
        # using JINJA templating engine that allows to inject variables in strings
        # bash_command='echo "{{ ds }}" "{{execution_date.strftime(\'%Y-%m\')}}"'
        # ds datetime timestamp just a  string. Importantis the execution date becuse its a timestmap.. we use the fucntion strftime() to format into string
        
    )
    
    
    
    format_to_csv_task = PythonOperator(
    task_id="format_to_csv_task" ,
    python_callable= format_to_csv,
    op_kwargs={
        "src_file": f"{OUTPUT_FILE_TEMPLATE}"
    }
    ,
    )
    
    
    ingest_task = PythonOperator(
    task_id="ingest",
    python_callable= ingest_callable,
    op_kwargs=dict(
            user= PG_USER,
            password= PG_PASSWORD,
            host= PG_HOST,
            port= PG_PORT,
            db= PG_DATABASE,
            tablename= TABLE_NAME_TEMPLATE,
            csv_file= CSV_FILE_INPUT
            )
    
    ,
    )

   
# we need to specify the dependency

wget_task >> format_to_csv_task >> ingest_task