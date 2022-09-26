#!/usr/bin/env python
# coding: utf-8
import os
import argparse
import sys
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
import pyarrow
from time import time
# get_ipython().system('{sys.executable} -m pip install pyarrow')

# df = pd.read_parquet('yellow_tripdata_2021-01.parquet')
# csv_name= 'yellow_trip_data.csv'




def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    tablename=params.tablename
    url=params.url
    parquet_name= 'output.parquet'
    
    
    # download parquet, convert to csv
    URL="http://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    os.system(f"wget {URL}  -O {parquet_name}")
    
    engine=create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")  # connecting to the docker postgres locally
    
    df=pd.read_parquet(parquet_name) #engine='pyarrow')
    
    
    csv_name='output.csv'
    df=df.to_csv(csv_name, index=False)
    

    df_iter=pd.read_csv(csv_name, iterator=True, chunksize=100000)




    df=next(df_iter)


    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)


    df.head(n=0).to_sql(name=tablename,con=engine, if_exists='replace') # for column heads



    df.to_sql(name=tablename,con=engine, if_exists='append') # for the 1st 100000 chunks


    while True:
        t_start=time() #timestamp at the beginning
        
        df=next(df_iter)
        
        df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=tablename,con=engine, if_exists='append')
        
        t_end=time()
        
        print('inserted another chunk ... , it took %.3f seconds'%(t_end-t_start) )


if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')



    # user, password, host, port, database name, table name, url of csv
    parser.add_argument('--user',help='user name for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--tablename',help='name of table where we will write the results to')
    parser.add_argument('--url',help='link of the csv file')
                        

    args = parser.parse_args()
    
    
    
    main(args)