# **THIS IS WEEK TWO OF DATA ENGINERING STEP BY STEP**

## DATA LAKE
* A data lake is central repo that holds big data from many sources.

* Data can be structured; semi-structured or unstructured.

* Idea is to ingest data as quickly as possible and make it availbale or accessible to other team members DAs,DSs,DEs.
* a data lake  _solution_ has to be secure and can scale.Hardware should be inexpensive.

#### Data Lake Vs Data Warehouse.

Data lake is unstructerd and can be used by data scientists and analysts.
* It is very large and can come in form of TBS and petabytes.
* ##### USE CASES
1. Stream Processing
2. Machine Learning
3. Real time analytics


Data Warehouse is structured and can be used by Business Analysts.
* Data size is generally small and 

* ##### USE CASES 
1. Batch Processing
2. BI reporting

* Usefullness of data has increased overtime. Use of a data lake allows quick accssbility.


## ETL vs ELT

* ETL - Export Transform Load -- used for small amount of data-- data warehouse sol. (schema on write)
* ELT - Export Load Transform -- large amount of data -- data lake sol.

ETL provides data lake support (Schema on read)

### Gotchas of Data Lake 

- Converts into a data swamp,makes it very hard to use.
- Incompatible schemas for same data without versioning
- No versioning
- No metadata assocciated 
- Joins are not possible (SQL) no available foreign key

#### CLoud Provider for Data Lake

GCP -cloud storage
AWS - s3
AZURE - Azure Blob

## Workflow Orchestration

Ideally what we want to do is to split the data into multiple files. Eg.

1. Download data
2. Ingest csv/parquet to postgres

A data pipeline can be split into 2 above steps. The pipelines are paramterized.

- The download data pipeline has the `url params` an therefore the data pipeline can be used to download  a different url. _reran_

- Alternatively, in the case of ny-taxi-data it could be parametarzied in terms of months. And the pipeline can be reexecuted for different months.

### How To Do This?
 * We can write 2 python scripts and 1 bash script -- not super convenient because we have to use the retry logic when certain steps fail due to internet connections and other irregularities.

 * We can use the `MAKE` utility  that allows to specify dependecies say the `ingest.py` scripts depends on `wget.py`. It will arrange thing in order.

 Data Pipeline jobs could be like. as called DATA WORKFLOW alias DAG (directed acyclic graph)

 ```WGET ---> PARQUETIZE ---> UPLOAD TO GCS ---> UPLOAD TO BIGQUERY---> {{TABLE IN BIGQUERY}}```

 These data workflow has some parameters.. Generic could be month.
 Then the different scripts have their parameters.


 #### DATA WORKFLOW ORCHESTRATION

 * Tools created specifically for defining data workflows. e,g **LUIGI**, **APACHE AIRFLOW**, **PREFECT**, **ARGO**.
 * Any data workflow orchestration tool that allows to specify our data workflows parametize them and rerun and so on.
* They let you specify the dependecy graph and the individual steps in the sequence of steps.


# APACHE AIRFLOW
* How to set up airflow environment with docker.
* Build and Ingestion pipeline to upload raw data to data lake.

* Query the data in GCP.

## AA Architecture.

Consists of the following:
 - _A web server_ - a handy GUI to inspect, trigger and debug the behaviour of DAGs and tasks. Available on localhost 8080
 - _Schecudler_ -A component responsible for scheduling jobs and it handles both triggering and scheduling workflows, submits tasks to the executor to run, monitors all DAGs and then triggers the task instances once their dependecies are complete.

 - _Worker_ - A component that executes the tasks given by the  scheduler

 - _Metadata Database_ - A backend to the airflow env. and it is used by the scheduler, executor and web server to store the state of the environment.

 In the docker compose service there are other services such as the redder service that fowards messages from the scheduler to worker. A flower app for monitoring the env. available on localhost 5555. An an airflow init service which is an initialization service custom to this workshop's design which initializes  the configs. such as backend, user credentials, env. variables etc.

 ### Setup of Airflow Env. Using Docker
 Rename the service account keys created from previous week to google credentials.json
 
 - Store in a path called `~/.google/credentials/` after moving it and renaming it google_credentials.json. This is important to maintain some standaradization accross our workshop setup.

 - We also need a docker compose cli tool possibly higher than V2 .just do wget [docker-compose](https://github.com/docker/compose/releases/download/v2.11.1/docker-compose-linux-x86_64)

 - Making docker-compose visible from any directory. We add it to the path variable
 we use `nano .bashrc` THEN 
 ```export PATH="${HOME}/bin:${PATH}"```

 Docker DESKTOP Docker needs virtualization for work.


### Airflow Set User
 - Create a new sub-directory called `airflow`
 - Download official apache-airlflow docker image run

 ```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.4.0/docker-compose.yaml```

 We get the offical setup provided by airflow. but skip and focus on the mains. CAn also create nofrills.yml


 Now set the airflow user. On linux the quick-start needs to know your host user-id and needs to have group id set to 0. Otherwise the `dags` , `logs`, `plugins` will be created with root user. Make sure to configure them for docker-compose,

 so
 ```mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" >.env
```
The .dags folder is where airflow pipelines are stored.
The .logs stores all log related info comms between schedulars and the workers.
The .plugins are for any custom plugins or helper functions that may be needed within dags.


### Docker Build 

- Build a custom docker file and use base image from the tag in the docker-compose yml downloaded.

There is a difference between `docker-compose` and `docker compose`.
Use docker compose for your case. You will only need to use the build command whenever there is any change in the Dockerfile

* Initialize the airflow scheduler, DB, and other config

use `docker compose up airflow-init`
Initializes your aiflow backend  and other env variables. And also configs, the DAGS,PLUGINS, ETC to your airflow docker container. 

* It makes use of the airflow credentials provided by official airflow setup.

* After init has been done there will be a success code 0 and then kick up all other services of the container. That is the backednd, schedulers and workers, webservers etc.

* Use webserver to acces airflow's UI. PASS DEFAULT SET OF CREDETNIALS PROVIDED IN THE OFFICIAL SETUP.