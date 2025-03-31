import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import os



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name
    parquet_name='input.parquet'
    csv_name= 'output.csv'

    os.system(f'wget {url} -O {parquet_name}')


    # Dowload the parquet file
    print("Reading Parquet file...")
    df = pd.read_parquet(parquet_name)

    df.to_csv(csv_name, index=False)

    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter =pd.read_csv(csv_name,iterator=True, chunksize=1000000)

    df = next(df_iter)

    df.head(n=0).to_sql(name=table_name,con=engine, if_exists='replace')

    while True:
        t_start = time()
        df = next(df_iter)

        df.tpep_pickup_datetime= pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime= pd.to_datetime(df.tpep_pickup_datetime)

        df.to_sql(name=table_name,con=engine, if_exists='append')

        t_end =time()


        print('Successfully inserted another chunk ..., and it took %.3f secs' %(t_end- t_start))



if __name__ == '__main__':

# parser for command line arguments, host and port are optional
    parser = argparse.ArgumentParser(description='Convert parquet to csv and ingest to postgres')

    #user, host, port, password, databasename, parquert url, tablename

    parser.add_argument('--user',help='Username for postgres database')      
    parser.add_argument('--password',help='Password for postgres database') 
    parser.add_argument('--host',help='Localhost for postgres database') 
    parser.add_argument('--port',help='Port for postgres database')
    parser.add_argument('--db',help='Database name postgres database') 
    parser.add_argument('--table_name',help='Table name postgres database')  
    parser.add_argument('--url',help="Parquet urL")      

    args = parser.parse_args()
    # print(args.accumulate(args.integers))

    main(args)

