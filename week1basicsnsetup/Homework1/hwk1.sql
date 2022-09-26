-- Q1.How many taxi trips were there on January 15?

SELECT count(*) FROM yellow_taxi_data
WHERE tpep_pickup_datetime::date= '2022-01-15'


-- Q2: On which day was there the largest tip amount

SELECT date_trunc('day',tpep_pickup_datetime) as day 
       ,max(tip_amount)
FROM yellow_taxi_data
GROUP by 1 
ORDER BY 2 DESC
LIMIT 1;

-- Q3: Most popular destination for passengers picked up in central park on Jan 14th

SELECT COALESCE(zd."zone",'Unknown') as zone
	  ,COUNT(*) as no_trips
FROM yellow_taxi_data y
 JOIN zones zu
ON y."PULocationID"=zu."LocationID"
LEFT JOIN zones zd
ON y."DOLocationID"=zd."LocationID"
WHERE zu."zone" LIKE '%central  park%' 
AND tpep_pickup_datetime::date= '2022-01-14'
GROUP BY 1 
ORDER BY 2 desc
LIMIT 1


-- Question 6  Get the max avg total amount paid in an pickup drop off pair and add Unknown if field is null.

SELECT  CONCAT (COALESCE(zu."Zone",'Unknown'),'/', COALESCE(zd."Zone",'Unknown'))
		,AVG(y.total_amount) as avg_tot_amount
FROM yellow_taxi_data y
LEFT JOIN zones AS zu
ON y."PULocationID"=zu."LocationID"
LEFT JOIN zones zd 
ON y."DOLocationID"=zd."LocationID" 
GROUP BY 1 
ORDER BY 2 DESC
LIMIT 1;