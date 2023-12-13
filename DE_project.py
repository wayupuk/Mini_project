
import boto3
import pandas as pd
from io import StringIO , BytesIO
from prefect import task,flow
import os
import psycopg2
from datetime import datetime
from sqlalchemy import create_engine
session = ''
test2 ="test5"
s3_client = boto3.client("s3")
bucket_ali = 'fullstackdata2023'
data_range = {}
arr = []
data = []
@task(retries= 3,log_prints=True)
def date_info():
    first_date = '2023/11/30'
    date_start = str(input("start date in y/m/d: "))
    date_end = str(input("end date in y/m/d: "))
    d0 = datetime.strptime(first_date, "%Y/%m/%d")
    d1 = datetime.strptime(date_start, "%Y/%m/%d")
    d2 = datetime.strptime(date_end, "%Y/%m/%d")
    if int(date_start[:4]) >= 2023:
        datediff = abs(d2-d1).days
        start = abs(d1-d0).days
        end = (abs(d2-d0).days)+1 
        print("start index: ", start)
        print("end index: ", end)
        return datediff,start,end

source_p = "******"

postgres_info = {
    'username': '*****',
    'password': '*****',
    'host': '******',
    'port': '*****',
}

    
@task(log_prints=True)
def  get_path(datediff,start,end):
    listdata = s3_client.list_objects(Bucket = bucket_ali ,Prefix = source_p )
    print(f"date different:  {datediff} index  use {datediff +1} days")
    for i in range(start,end+1):
        file_path_date = listdata['Contents'][i]['Key']
        data.append(file_path_date)
    print(f"before pop first index: {data[0]}")
    data.pop(0)
    
    print(f"first transaction path: {data[0]}")
    print(f"last transaction path: {data[-1]}")
    return data

@task
def extract(bucket_name,data):
    n = 0
    for p in data:
        respone = s3_client.get_object(Bucket = bucket_name , Key = p)
        csv_string = StringIO(respone['Body'].read().decode('utf-8'))
        data_range["df{0}".format(n)] = pd.read_csv(csv_string)
        n +=1
    return data_range


@task
def concat(data_range):
    for i in data_range.values():
        arr.append(i)
    customers = pd.concat(arr,ignore_index= True)    
    return customers
        
@task(log_prints=True)
def tranform(df):
    customer_cols = ['customer_id','customer_name','customer_province']
    join_core = ['customer_id','date']
    revenue_core = ['customer_id','total_revenue']
    qty_core = ['customer_id','qty']
    customers = df[customer_cols].drop_duplicates()
    customers = customers.reset_index()
    
    recency_join = df[join_core]
    recency_join_format = recency_join.groupby('customer_id')['date'].max()
    # df_recency = pd.DataFrame(recency_join_format).reset_index
    recency_join_format = recency_join_format.reset_index()
    recency_join_format.columns = ['customer_id','recency']
    
    revenue = df[revenue_core]
    revenue_join_format = revenue.groupby('customer_id')['total_revenue'].sum().round(2)
    revenue_join_format.columns = ['customer_id','revenue']
    
    qty_join = df[qty_core]
    qty_join_format = qty_join.groupby('customer_id')['qty'].sum()
    qty_join_format.columns = ['customer_id','total_qty']
    
    df_merge = customers.merge(recency_join_format,how='left',on='customer_id')
    df_merge = df_merge.merge(revenue_join_format,how='left',on='customer_id')
    df_merge = df_merge.merge(qty_join_format,how='left',on='customer_id')
    print(f"first 5 row{df_merge.head()}")
    print(f"last 5 row{df_merge.tail()}")
    return df_merge

###print(s3_client.list_buckets())

@task
def load(df_name,name):
    target_path = f'damonida16/customer/{name}.parquet'
    parquet_Buffer = BytesIO() 
    df_name.to_parquet(parquet_Buffer,index=False )
    s3_client.put_object(Bucket = bucket_ali, Key = target_path , Body = parquet_Buffer.getvalue())
    print('upload sucessfilly')
    
@task(log_prints=True)
def show(df):
    print(df.head())
    print(f'shape{df.shape[0]}')

@task 
def load_postgres(customer):
    '''2
    Load transformed result to Postgres
    '''
    database = postgres_info['username'] # each user has their own database in their username
    table_name = 'customer'
    database_url = f"postgresql+psycopg2://{postgres_info['username']}:{postgres_info['password']}@{postgres_info['host']}:{postgres_info['port']}/{postgres_info['username']}"
    engine = create_engine(database_url)
    print(f"Writing to database {postgres_info['username']}.{table_name} with {customer.shape[0]} records")
    customer.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Write successfully!")
@flow 
def pipline():
    datediff,start,end = date_info()
    data = get_path(datediff,start,end)
    data_range = extract(bucket_ali,data)
    customers = concat(data_range)
    lcustomers = tranform(customers)
    show(lcustomers)
    load_postgres(lcustomers)
    # load(customers,test2)

if __name__ == '__main__':
    pipline()
    # pipline.serve(name="f_pipeline")

# lists = s3_client.list_objects(Bucket = bucket_ali ,Prefix = source_p )
# ka = lists['Contents']
# print(ka)