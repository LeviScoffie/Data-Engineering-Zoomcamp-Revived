
import os

import sys
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
import pyarrow
from time import time
# get_ipython().system('{sys.executable} -m pip install pyarrow')

# df = pd.read_parquet('yellow_tripdata_2021-01.parquet')
# csv_name= 'yellow_trip_data.csv'




def ingest_callable(user, password, host, port ,db, tablename, parquet_file):
    print(tablename, parquet_file)
    
    
    
    
    # download parquet, convert to csv
  
    engine=create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")  # connecting to the docker postgres locally
    engine.connect()
    
    print('connection establsihed successfully, inserting data')
    
    # df=pd.read_parquet(parquet_name) #engine='pyarrow')
    
    
    # csv_name='output.csv'
    # df=df.to_csv(csv_name, index=False)
    
    t_start=time()
    
     df_iter=pd.read_parquet(parquet_file, iterator=True, chunksize=100000) # to check if can make a DAG

    df=next(df_iter)


    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)


    df.head(n=0).to_sql(name=tablename,con=engine, if_exists='replace') # for column heads



    df.to_sql(name=tablename,con=engine, if_exists='append') # for the 1st 100000 chunks
    
    t_end=time()
    print('inserted the first chunk , took %.3f seconds'%(t_end-t_start) )
    
    
    
    while True:
        t_start=time() #timestamp at the beginning
        
        df=next(df_iter)
        
        df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=tablename,con=engine, if_exists='append')
        
        t_end=time()
        
        print('inserted another chunk ... , it took %.3f seconds'%(t_end-t_start) )

