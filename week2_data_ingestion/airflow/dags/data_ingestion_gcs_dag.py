import os
import logging


from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

## FROM THE REQUIREMENTS INSTALLED THROUGH THE requirements.txt file when build docker conatiner.
from google.cloud import storage #to interact with gcs storage

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator # to interact with bigquery ino
#inorder to create an external table
import pyarrow.csv as pv # convert dataset into parquet before converted to gcs. but not needed since already in parquet.
import pyarrow.parquet as pq


#import some values from env variables in docker-compose yml. setup into our local variables.
PROJECT_ID= os.environ.get("GCP_PROJECT_ID")
BUCKET= os.environ.get("GCP_GCS_BUCKET")

dataset_file= "yellow_tripdata_2021-01.parquet"
dataset_url= f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}"
path_to_local_home = os.environ.get("AIRFLOW_HOME","/opt/AIRFLOW/")
parquet_file=dataset_file #.replace('.csv','.parquet') #to be used incase fiil is csv.
BIGQUERY_DATASET = os.environ.get ("BIGQUERY_DATASET",'trips_data_all')


#todo incase file is csv and want to convert it to parquet def fxn operator:Takes an input
# of a source file and converts it to a parquet format
# def format_to_parquet (src_file):
#     if not src_file.endswith('.csv'):
#         logging.error("Can only accept source files in csv format, for the moment")
#         return
    
#     table = pv.read_csv(src_file)
#     pq.write_table(table, src_file.replace('.csv','.parquet'))
    
    
# c
def upload_to_gcs (bucket, object_name, local_file):
    
    """
    Ref: from gcs to include linke
    :param bucket: GCS bucket name
    :param object_name: target path & file_name
    :param local_file : source path & file_name
    
    :return:
    """
    
    # WORKAROUND to prevent timeout for files > 6MB on 888kbps upload speed
    # ref googleapis/python/github.com
    storage.blob._MAX_MULTIPART_SIZE= 5 * 1024 * 1024 #5mb
    
    storage.blob._DEFAULT_CHUNKSIZE= 5 * 1024 * 1024 #5mb
    #END OF WORKAROUND
    
    # if BUCKET:
    #     STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        
    client = storage.Client() # creates a client for gcs storage
    bucket = client.bucket(BUCKET) # attaches itself to a bucket that u are passing as an input
    
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file) # uploads file that it is supposed to uplooad to a target location
    
    
    
  #ref:  
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

#NOE: DAG declaration - using a Context Manager (an implicit way)

with DAG(
    dag_id = "data_ingestion_gcs_dag",
    schedule_interval = "@daily",
    default_args =default_args,
    catchup = False,
    max_active_runs = 1,
    tags= ["dtc-de"],
    
) as dag:
    
# WORKFLOW BEGINS:

#1. download dataset task

    download_dataset_task = BashOperator (
        task_id="download_dataset_task",
        bash_command =f"curl  -sSL {dataset_url} > {path_to_local_home}/{dataset_file}"
    )
    ## Once dowloaded it could stores itself into: 
    # if using a  managed service for airflow env it stores in memory
    # if using docker env. it will store in one of the temp locations or specified dir for the file downloaded.
    # converts to parquet format but not needed at the moment since data set is parquet arealdy
    # format_to_parquet = PythonOperator(
    # task_id="format_to_parquet_task"    ,
    # python_callable= format_to_parquet,
    # op_kwargs={
    #     "src_file": f"{path_to_local_home}/{dataset_file}"
    # }
    # ,
    # )
    # uploads paquet file to expected gcs location
    local_to_gcs_task = PythonOperator (
        task_id  ="local_to_gcs_task",
        python_callable =upload_to_gcs,
        op_kwargs ={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
        
    )
    
    # refers to source file tht was uploaded to the gcs, extract schema and create an exteranl table
    # based on that. IN A MORE READBLE FORMAT
    
    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{parquet_file}"],
            },
        },
    )
    
    ## DEFINE WORKFLOW OF HOW DIRECTION OF TASKS SHOULD BE
    
    download_dataset_task  >> local_to_gcs_task >> bigquery_external_table_task
    
    # >> format_to_parquet