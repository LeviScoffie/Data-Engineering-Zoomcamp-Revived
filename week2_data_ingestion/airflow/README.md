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

* After init has been done there will be a success code 0 and then kick up all other services of the container
using `docker compose up`. That is the backend, schedulers and workers, webservers etc.

* Use webserver to acces airflow's UI. PASS DEFAULT SET OF CREDETNIALS PROVIDED IN THE OFFICIAL SETUP.

### THE ANATOMY OF A DAG
- Check the typical work flow components,  and write out ingestion pipeline to ingest some compressed raw data to a data lake.

4 main components of a workflow:
* DAG - Directed Acyclic Graph that specifies the dependecies between a set of tasks with explicit execution order.
* Task - A defined unit of work alias _operators and airlfow_. They descirbe what to do; be it fetching the data, running analysis, triggering other systems etc.
* DAG Run- Individual execution or run of a DAG
* Task Instance - Individual run of a single task. Also have an indicative state which could be running succesfully


#### DAG STRUCTURE
An airflow dag is defined in a python script. Composed of a dag definition, tasks e.g operators, and task dependecies.

When declaring a DAG we use an implicit way using a **context manager**

A DAG runs through a series of tasks and there are three common types of tasks i.e:
 - Operators - these are predefined tasks that u can string together quickly to build most part of dags.
 - Sensors - A special subclass of operators that are entirly about waiting for an external event to happen.
 - A task flow decorator - custom python fxn packaged up as a task.

 Tasks are defined based on the abstraction of operators which rep a single ..

 Atomic operators are best becasue they do not need to share resources and therefore can stand on their own. You can chose a python operator() , bash operator() or any other operators provided  by a client or a respiurce you're using such  as google.

 Aiflow is agnostic to wht u are using.

 Every single operator must be defined to a DAG. Either using a `with` operator or by passing a DAG_ID into each of the operators or tasks.

 Parameterizing DAGs always includes an interval.
 There are also default arguments inside a DAG. And many DAGs need the same set of default arguments e.g start_date.

 Rather than having to specify that individually for every operator, you can call it early in the script and will be auto applied to any operator tied to it.


 ##### Task Dependecies.
 Responsible for the control flow within  a DAG.
 A task operator does not usually live alone.It has dependecies on other tasks.

 The declaration of these dependecies are done with bit shift operators such as `>>`.
 By default a task will run when all its upstream parent tasks have succeeded.

 To pass the data between tasks, we have 2 options;
  - **XCOM variable** - a system that can have tasks   push and pull small bits of metadata.
  - Updload and Download large files from a storage service.

Airflow sends out tasks to run on workers as space becomes available so there's no guarantee all the tasks in your dag will run on the same worker or on the same machine.

There are also features for letting you easily pre-configure access to a central resource like a data source in the form of connections and hooks.


##### DAG RUNs
In two ways:
- Triggering manually or via API.
- Schedule then using the schedule interval variable.

A new instance of a DAG is created every time a DAG is run. DaG runs can be in parallel for the same dag  and each has a defined data interval also defined by the execution date which defines the period of the data the task should operator on.

This is useful in cases where airflow can backfill the DAG and run copies of it for every day in those previous runs.


##### Task Instances.
An instance of a task is a specific run of DAG task for a given Dag AND thus for a given data interval. There are also reps of a task that has state reppn what stage of the life cycle it is in.
Some of task instaces include: _none, scheduled,queued,running, success, failed, upstream-failed_ .
Ideally: none>>scheduled>>queued>>running>>success.

## DAGIFY WEEK1 
- We now want to take the ingestion scprit that we did in week 1 and put it in a data pipeline to automate the whole process of ETL.

PLAN
* Start with the docker-compose from week2
* Chnage the DAG mappings
* Create a new DAG with two dummies
* Make then run monthly
* Create a bash operator , pass the params(`execution date strfitime (% Y-%m))
* Download the data
* Put theingestion script to airflow
* Modify dependcies-add ingest script dependencies
* Put the old docker compose file in the same network.

1. Use the downloaded docker compose yml file. Just change the volume mapping becasue the intial dag folder contain the py scipt that was used to ingest data into gcs. Contained the workflow for uploading data to gcs bucket.

We now want to ingest the data to a local DB . ie. postgres. AND The steps mentioned above are what we are going to follow.

* Create a new folder `dags_new` and start from scratch. No prior history of other dags. 

* In docker-compose file map the dags_new volume to it. Also switch the .env file abit to match the postgres.

* Do due processes and the foward the webserver port.Open the webserver and there are no dags because the mappings were in a new directory in docker compsoe file


### CREATING A DAG.
* Cretea a py file.
* Import DAG defintions then the BASH and Python Operators.

* To create a task we use the operators.

 **[READ COMMENTS ON PY SCRIPT]**

 The schedule interval can be cron expersion. We can use the crontab guru. Think through how we want to execute the job.
 In thec case of montlhy, from JAN to FEB to MARCH.
 * Say now we collect data of JAN and wait a bit to process it and process it in FEB  2nd and so on and so forth.
 * WAit for a month to be over then execute processing of the data on the 2nd of each month.
 * Using cron tab guru every 2nd day of the month at 7:00 am we schedule our job. and process all data collected over the previous month.

 * The logs on airflow webserver show how the code peforms and thge codes and commands executed. Tasks executed in correct order. 
 * We use a bash operator to download the file. Remote machine its faster. which I am using currently,.

 * While running DAG we find that there is no wget so we can install it in dockerfiile and do dockercompose up all over again. Or we can use curl instead.

 * Not good to qrite to output.csv. This is because when running the DAGS, there may be overwring whicha may corrupt a file. We want each task to write to its own output file.

 `{{ execution_date.strftime(\'%Y-%m\')` is what will differentiate the differnce datasets and we use it to parameterize the downloads. repalce in src linke. Its a truncation of the date timestamp to e.g `2021-01`.


 * Puting the ingestion script to airflow.
 * Create a  new file under dags_new directory and put all the logic of processing the csv file there

 * `--no-cache-dir` in dockefile it means that it will not save things to cache. hence it will skip that part.hence image is not large. so update the dockerfile beacue we will needs the pandas library to operate with in the Python Operator.

 #### HOW DO WE CONNECT 2 YAML FILES?
 run docker network ls

 ## todo VM memory and CPU cannot run airflow docker.

 * Go to airflow worker and then try to connect to the pg datbase of week 1 from the worker.
 - Run `docker exec -it (worker id container) bash` 
 - Run python
 - Use it to check for connection if the airflow worker can connect to a database that is outside airflow. Used docker compose networks ;
 ```from sqlalchemy import create_engine
 engine= create_engine(f"postgresql://{root}:{root}@{pgdatabase2}:{5432}/{ny_taxi}")
 engine.connect()
 ```

All the tasks in airflow should be idempotent. That is droppig database and creating a new one. Goodness of this line of code

` df.head(n=0).to_sql(name=tablename,con=engine, if_exists='replace')`