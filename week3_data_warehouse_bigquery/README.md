# DATAE WAREHOUSES

* OLAP vs OLTP
* What is a data warehouse
* BigQuery
    * Cost
    * Partitions and Clustering
    * Best Practices
    * Internals
    * ML in BiqQuery



## OLAP vs OLTP

OLTP- online transaction processing
OLAP- online analtyical processing


OLTP used in databases for backednservives. Groyuping SQL queries togethere. OLAP used for putting alot of data inside for analytical purposes.

OLTP fater upadates nd smaller data size.

OLTP productivity is increased for end users while OLAP efficiency is for data analysts and scientists.

A dat warehouse is an OLAP soln. used for reporting and data analysis. Consists of raw data, meta data, and summary.

Procedure:

Various data sources(i.e OS, OLTP databases, Others) > Staging Area > Data Warehouse > Data Marts > Users.

# BIGQUERY

This is a serverless data warehouse. There are no servers to manage or database software to install.

Provides software and infra helps in scalability and high-avaliablity.

Use a SQL interface to do ML.

BiqQuery maximizes flexibilty by separating the compute engine that analyzes your data from your storage.

BIGQUERY normally caches data. There is open source public data.

### BIGQUERY COST
On demand pricing 1tb OF data processed is $5

Flat rate pricing 100 slots > $2000/month = 400 TB data processed on demand pricing.


`gs://transfer-service-terraform-bucket/trip data/yellow_tripdata_2019-*.parquet`

`gs://transfer-service-terraform-bucket/trip data/yellow_tripdata_2020-*.parquet`
    


BIGQUERY and GCS are independent tools, thus data from GCS is treated as external data


