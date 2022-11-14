-- --create a non-partioned table
CREATE OR REPLACE TABLE `loyal-glass-359906.nytaxi3.yellow_tripdata_non_partitioned` AS 

SELECT * FROM `loyal-glass-359906.nytaxi3.external_yellow_tripdata`

-- create  a partioned table
CREATE OR REPLACE TABLE  `loyal-glass-359906.nytaxi3.yellow_tripdata_partitioned` 
PARTITION BY DATE (tpep_pickup_datetime)
  AS 
SELECT * FROM `loyal-glass-359906.nytaxi3.external_yellow_tripdata`

--scanning impact of partioning 

--scanning 1.6gb of data 

SELECT DISTINCT(vendorID)
FROM loyal-glass-359906.nytaxi3.yellow_tripdata_non_partitioned 
WHERE date(tpep_pickup_datetime) between '2019-06-01' AND '2019-06-30';


--Scanning partioned data 
-- ~106MB of data 

SELECT DISTINCT(vendorID)
FROM loyal-glass-359906.nytaxi3.yellow_tripdata_partitioned 
WHERE date(tpep_pickup_datetime) between '2019-06-01' AND '2019-06-30';

--looking into partitions keenly. Helps to determine if you have bias in your partitions

SELECT table_name, partition_id, total_rows 
FROM `nytaxi3.INFORMATION_SCHEMA.PARTITIONS` 
WHERE table_name= 'yellow_tripdata_partitioned'
ORDER BY total_rows DESC;

--creating a partions and cluster table
CREATE OR REPLACE TABLE  `loyal-glass-359906.nytaxi3.yellow_tripdata_partitioned_clustered` 
PARTITION BY DATE (tpep_pickup_datetime)
CLUSTER BY vendorID
  AS 
SELECT * FROM `loyal-glass-359906.nytaxi3.external_yellow_tripdata`


-- scan diff between partioned table and partioned&clustred table
-- Query scans ~1.06gb
SELECT COUNT(*) as trips
FROM `loyal-glass-359906.nytaxi3.yellow_tripdata_partitioned`
WHERE date(tpep_pickup_datetime) between '2019-06-01' AND '2020-12-31'
AND VendorID=1;


-- partitioned and clustered table
SELECT COUNT(*) as trips
FROM `loyal-glass-359906.nytaxi3.yellow_tripdata_partitioned_clustered`
WHERE date(tpep_pickup_datetime) between '2019-06-01' AND '2020-12-31'
AND VendorID=1;




