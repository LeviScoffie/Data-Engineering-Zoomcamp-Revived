-- create a table in a dataset sourcing data from gcs
CREATE OR REPLACE EXTERNAL TABLE `loyal-glass-359906.nytaxi3.external_yellow_tripdata`
OPTIONS(
  format='CSV',
  uris=['gs://transfer-service-terraform-bucket/csv_backup/yellow_tripdata_2019-*.csv',
  'gs://transfer-service-terraform-bucket/csv_backup/yellow_tripdata_2020-*.csv']
);

--inspecting the table
SELECT * FROM `nytaxi3.external_yellow_tripdata` LIMIT 110;