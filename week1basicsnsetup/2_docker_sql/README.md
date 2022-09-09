services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    restart: always

## Postgres

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
 postgres:13

## specify environment variables
## mounting
## specify the port( sending requests to the database)

https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page # Actual data

https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf  # Data dictionary

https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv   # Taxi Zone Lookup Table




## PGAMDMIN


docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
 dpage/pgadmin4


 ## NETWORK

 docker network create pg-network

 docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database-2 \
 postgres:13


docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin-2 \
dpage/pgadmin4



URL="http://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
python ingest_data_2.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --tablename=yellow_taxi_data \
  --URL=${URL}   


docker build -t taxi_ingest_2:v001 .


URL="http://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
docker run -it \
--network=pg-network \
taxi_ingest_2:v001 \
  --user=root \
  --password=root \
  --host=pg-database-2 \
  --port=5432 \
  --db=ny_taxi \
  --tablename=yellow_taxi_data \
  --URL=${URL}   


  ## Docker Compose 

  services:
  pgdatabase2:
    image: postgres:13
    environment:
    - POSTGRES_USER=root
    - POSTGRES_PASSWORD=root
    - POSTGRES_DB=ny_taxi
    volumes:
    
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root

    ports:
      - "8080:80"


      docker-compose up 
   __or__
      docker-compose down 

      docker-compose  up -d   --run in detach mode 


## GCP & TERRAFORM

Create service account and retrieve keys that are  in json form

sudo snap install gcloud --classic


- To set google applications environment variable which is system specfifc to a service account.

- run  export GOOGLE_APPLICATION_CREDENTIALS=/home/leviscoffie/Downloads/loyal-glass-359906-d8498db322d5.json
  
#### O auth authentication method

- run gcloud auth application-default login 

to authenticate. To enable your local to be able to interact with the cloud evironment.



### CREATE INFRASTRUCTURE FOR PROJECT WITH TERRAFORM

- Create two resources in googl environement that is;

  * Google Cloud Storage (GCS): Data Lake- you can store date in flat file manner. All raw data is stored in a more organized fashion partitoned by more sensibles directories. parquet,json,csv
  * Big Query : Data Warehouse- Dta is modelled into a more structured format with fact and dimension tables. Classical Datawarehouse Concepts.


## Setup Access
1. IAM Roles for Service Account created.
    Storgae Admin, Storage Object, BiGQuerry Admin, Viewer.
2. Enable these APIs for your project:
    * [IAM API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
    * [IAM CREDENTIALS](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)

    
- Addiing permissions for our service account.