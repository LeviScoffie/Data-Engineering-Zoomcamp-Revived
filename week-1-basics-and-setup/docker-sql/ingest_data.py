#Cleaned up version of data-loading.ipynb
import argparse, os, sys
from time import time
import pandas as pd 
import pyarrow.parquet as pq
from sqlalchemy import create_engine



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tb = params.tb
    url = params.url
    
    # Get the name of the file from url
    file_name = url.rsplit('/', 1)[-1].strip()
    print(f'Downloading {file_name} ...')
    # Download file from url
    os.system(f'curl {url.strip()} -o {file_name}')
    print('\n')

    # Create SQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read file based on csv or parquet
    if '.csv' in file_name:
        df = pd.read_csv(file_name, nrows=10)
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
    elif '.parquet' in file_name:
        file = pq.ParquetFile(file_name)
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else: 
        print('Error. Only .csv or .parquet files allowed.')
        sys.exit()

    df.head(n=0).to_sql(name=tb,con=engine, if_exists='replace')

    # Insert values
    t_start = time()
    count = 0
    for batch in df_iter:
        count+=1

        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch

        print(f'inserting batch {count}...')

        b_start = time()
        batch_df.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time()

        print(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')
        
    t_end = time()   
    print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    





if __name__ == '__main__':

# parser for command line arguments, host and port are optional
    parser = argparse.ArgumentParser(description='Convert parquet to csv and ingest to postgres')

    #user, host, port, password, databasename, parquert url, tablename

    parser.add_argument('--user',help='Username for postgres database')      
    parser.add_argument('--password',help='Password for postgres database') 
    parser.add_argument('--host',help='Localhost for postgres database') 
    parser.add_argument('--port',help='Port for postgres database')
    parser.add_argument('--db',help='Database name postgres database') 
    parser.add_argument('--tb',help='Table name postgres database')  
    parser.add_argument('--url',help="Parquet urL")      

    args = parser.parse_args()
    # print(args.accumulate(args.integers))

    main(args)

