### Week 3 - Problem Statement
1. Workflow design (week3/READMe.md)
    1. Problem Statement:
        * Automating with Airflow pipeline
        * DAG: `GCS -> BQ (External table) -> BQ (PARTITIONING)

 use data ingested in gcs. 
 partitioning- enhance perfomance
 * Going to use the lightweight version because of compute issues. 

* IF you are using a custom setup, then u need a custome entry point script as well.

* We dont have any custom helper functions therefore we dont really need the **plugins** directory.

* One of the airflow config variables is "execution_date.()"

Decided to use the lightweight version of airflow in week3.

There is a manual config needed for this execise hence the entrypoint.sh script - it manually creates our account for logging in to airflow env.

We create 2 parallel workflows for the yellow and green tripdata. Eahc of them has tasks for creating an external table, then a partiontable based on that.


Had to use `sudo chown -R {myuser}` so that I could edit files while in the VM instance.

Name the .py wth  suffix **dag** keyword to optimize the airflow config. to find the word dag and work on it


## In the DAG.py  script
- No format conversions since these operations will be cloud-based.

- No need for Bash and Python Operators because we dont need to write any custom  functions that are turned into taks..just using the google provide ones.

- No need for the dataset file because we will be just importing the files loaded on GCS earlier in this [repo](https://github.com/LeviScoffie/DAG-creation).



### Steps in this dag creation 

1. Outline the main tasks that are needed to be done.
2. Gcs to gcs task that would reorganize the folder structure better.
3. Create 2 external tables based on the colors of the taxis.
4.  Prepare external tables pointin to the earlier created directories.


Airflow provides google integrated libraries for writng operators and other tasks. e.g "transfer service" which we will use to reorganize the GCS files.


The point of using `BigQueryInsertJobOperator` class helps you create an operator that can execute any sql query including DDL statements and DML statemtns.

> DDL stands for Data Definition Language. DML stands for Data Manipulation Language. DDL statements are used to create database, schema, constraints, users, tables etc. DML statement is used to insert, update or delete the records.

With the class you can define a variable with a DML query Then put it into the `BigQueryInsertJobOperator` to do the operation
