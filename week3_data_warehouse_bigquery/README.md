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

### PARTITIONS IN BIGQUERY
When we create a dataset, we have certain colummns like creation date, title of question and tags. i.e stackoverflow questions dataset

Assuming that most of the queries are based upon date and use it as a filter. E.g give all questions given in first week of match.

A partiotion table is partitioned by the date, this powerful for BG. Reads and processes data fro only that specific date and drastically reduces our costs.

Once you partion a dataset, the dataset now becomes a part of bigquery storage and now the dataset's meta data such as its size and other storage details can be accessed. And the column it is partioned by. Helps identify if there is bias in our partitions based on the number of rows.


### CLUSTERING IN BIGQUERY
After partioned based upon date, we can cluster based on a tag. So withi a partition, data can be clusterede based upon another field such as tag. Helps imporve cost and query perfomance.

On taking the partioned table, we can cluster it by vendor ID. The information is all gathered in the storage information of BIGQUERY.

When you create a partition table you can choose between a time unit column, ingestion time or an integer range partitioing.

#### In depth partitioning
* Through ingestion time you can truncated based on daily, monthly, hourly, etc. Daily is more often.

* Choosing an hourly partition is recommended incase you have a huge amount of data coming in, and you want to pricess it based upon each hour. BQ limits number of partitions to 4000. 


#### In depth clustering
* Columns you specify are used to colocate related data
* Order of the column is important
* The order of the specified columns detrmines the sort order of the data.
* Clustering improves 
    * Filter queries
    * Aggregate queries 

* Table with data size< 1gb dont show significat imporovement with clusyering and partioning.
* You can specify up to four clustering columns.


Clustering columns can fall into these top-level non-repeated columns types 

    * date 
    * bool 
    * geography 
    * int 64 
    * numeric
    * bignumeric
    * string
    * timestamp
    * datetime

partition costs benefits are known upfront. vlustering is not enough.

Clustering provides more granularity which partioning cannot provide. 

There is partion-level management, e.g deleting, creating new partitions, moving them e.t.c these things are not possible within clustering

Partitioning done by single column, clustering can be done on multiple columns.

When cardinality of the nu,mber of values is alot.


### wen clustering > partitioning 

* Partitioning results in a small amount of data per partition (approx. less than 1GB)

* Partitioning results ina large number of partitions beyond the limits on partitioned tables 

* Partitioning results in your mutation operation modifying the majority of partitions in the tables frequently (e.g every few minutes)

_clustering strategy vs partitiioning strategy_

## AUTOMATIC RECLUSTERING 

* As data is added to clusters, the newly inserted data can be written to blocks that contain key ranges that overlap with the key ranges in previously written blocks

* These overlapping keys weaken the sort property of the table.

Therefore, to maintain performance x-stics  of a clustred table 
- BQ performs automatic reclustering in the background to restore the sort property of the table.
- For partitioned tables, clustering is maintained for data within the scope of each partition.

### BQ best practice 
* Cost reduction
  - Avoid `SELECT *` -BQ stores data in a columnar  storage. only seletecd colummns are read.
  - Price your queries before running them
  - Use clustered and Partioned tables 
  - Use streming inserts with caution -increase cost drastically
  - Materialize query results in stages - incase u are using a CTE multiple times you can materialize it and use it to for cost optimization.


* Query Performance 
    - Filter on partitioned columns 
    - Denormalizing data 
    - Use nested or repeated columns
    - Use external data sources approx.
    - Dont use it, in case u want a high query performance
    - Reduce data before using a JOIN 
    - Dont treat WITH clauses as prepared staements 
    - Avoid oversharding tables
    - Large tables first (rows) then fewest rows then place remaining tables by decreasing size.