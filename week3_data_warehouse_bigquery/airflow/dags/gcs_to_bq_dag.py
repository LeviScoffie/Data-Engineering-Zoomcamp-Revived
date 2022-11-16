import os
import logging


from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator # to interact with bigquery 
#inorder to create an external table
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator



PROJECT_ID= os.environ.get("GCP_PROJECT_ID")
BUCKET= os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME","/opt/AIRFLOW/")
BIGQUERY_DATASET = os.environ.get ("BIGQUERY_DATASET",'trips_data_all')


DATASET='tripdata'
COLOUR={'yellow':'tpep_pickup_datetime', 'green':'lpep_pickup_datetime'}
INPUT="raw"
FILETYPE="parquet"


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


with DAG(
    dag_id = "gcs_2_bq_dag",
    schedule_interval = "@daily",
    default_args =default_args,
    catchup = False,
    max_active_runs = 1,
    tags= ["dtc-de"],
    
) as dag:
    
    for colour, ds_col in COLOUR.items():
    
        move_files_gsc_task= GCSToGCSOperator(
            task_id=f"move_{colour}_{DATASET}_files_task",
            source_bucket=BUCKET, # because we have already assigned the gcs bucket id  here "BUCKET= os.environ.get("GCP_GCS_BUCKET")" in docker config. so we are just picking up the env. variable
            source_object=f"{INPUT}/{colour}_{DATASET}*.{FILETYPE}",
            destination_bucket=BUCKET,
            destination_object=f"{colour}/{colour}_{DATASET}",
            move_object=True,
            # gcp_conn_id=google_cloud_conn_id we dont need this becasue api configured in dockercompose.yml file
        )
            
        
        
        bigquery_external_table_task = BigQueryCreateExternalTableOperator(
            task_id=f"bq_{colour}_{DATASET}_files_task",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": f"{colour}_{DATASET}_external_table",
                },
                "externalDataConfiguration": {
                    "sourceFormat": "PARQUET",
                    "sourceUris": [f"gs://{BUCKET}/{colour}/*"],
                },
            },
        )
        
        # DROP_TABLE_COLUMN_QUERY=(f"ALTER TABLE {BIGQUERY_DATASET}.{colour}_{DATASET}_external_table\
        #     DROP COLUMNS IF EXISTS ['airport_fee']")
        
        
        # update_table_schema_task = BigQueryUpdateTableSchemaOperator(
        #     task_id="update_table_schema_task",
        #     dataset_id={DATASET},
        #     table_id="test_table",
        #     schema_fields_updates=[
        #         {"name": "emp_name", "description": "Name of employee"},
        #         {"name": "salary", "description": "Monthly salary in USD"},
        #     ],
        # )

        
        
        CREATE_PARTITIONED_TABLE_QUERY=(f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{colour}_{DATASET}_partitioned\
        PARTITION BY DATE ({ds_col})\
        AS \
        SELECT * EXCEPT (ehail_fee) FROM {BIGQUERY_DATASET}.{colour}_{DATASET}_external_table;"  #find a way to incooporate both green and yellow tripdata in one statement
        )   

        
        
        bq_create_partition_task = BigQueryInsertJobOperator(
            task_id=F"bq_create_{colour}_{DATASET}_partition_task",
            configuration={
                "query":{
                    "query": CREATE_PARTITIONED_TABLE_QUERY,
                "useLegacySql": False,
                
                }
                    
            },
        )
                
        
        
        
        move_files_gsc_task >> bigquery_external_table_task >> bq_create_partition_task