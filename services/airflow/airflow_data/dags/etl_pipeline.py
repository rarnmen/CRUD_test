import json
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime as dt
import pandas as pd
from functools import reduce
import psycopg2
import sys
import os
from dotenv import load_dotenv
import os

load_dotenv()
host = os.environ.get('HOST_POSTGRES')
database = os.environ.get('PASSWORD_POSTGRES')
user = os.environ.get('USER_POSTGRES')
password = os.environ.get('PASSWORD_POSTGRES')
port = os.environ.get('PORT_POSTGRES')

conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=5432
        )

default_args = {
    'owner': 'airflow',
}

@dag(dag_id="etl",default_args=default_args, schedule_interval="@once", start_date=days_ago(1), catchup=False)
def pipeline_etl():
    @task()
    def extract(orden_id: int):
        query = f"""SELECT * FROM raw_data.estado
                    WHERE orden_id={orden_id}"""
        
        df_estado = pd.read_sql_query(query, conn)

        query = f"""SELECT * FROM raw_data.orden
                    WHERE id={orden_id}"""
        
        df_orden = pd.read_sql_query(query, conn)
        return {"orden": df_orden, "estado": df_estado}
       
        
    @task()
    def transform(dict_):
        df_orden = dict_['orden']
        orden_id = df_orden['id'].values[0]
        df_estado = dict_['estado']
        latitude, longitud = tuple(df_orden['ubicacion'].values[0].replace('(','').replace(')','').split(','))
        latitude, longitud = float(latitude), float(longitud)
        tiempo_entrega = df_estado['tiempo_estado'].sum()
        productos = df_orden['productos'].values[0]
        productos = productos.replace('[','').replace(']','').split(',')
        print(productos)
        for i, producto in enumerate(productos):
            productos[i] = int(producto)

        return { 'orden_id': orden_id,'latitude': latitude, 'longitude': longitud,
                 'tiempo_entrega': tiempo_entrega, 'productos': productos}
 


    @task()
    def load_orden(dict_):
        query = 'INSERT INTO summary_data.ordenes (orden_id, latitud, longitud, tiempo_de_entrega) VALUES(%s, %s, %s, %s)'
        values = (int(dict_['orden_id']), float(dict_['latitude']), float(dict_['longitude']), int(dict_['tiempo_entrega']))
        cur=conn.cursor()
        try:
            cur.execute(query, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"error:{e}")
        cur.close()

    @task()
    def load_products(dict_):
        query = 'INSERT INTO summary_data.productos (orden_id, producto_id) VALUES(%s, %s)'
        values = []
        for product in dict_['productos']:
            values.append((int(dict_['orden_id']), int(product)))
        cur=conn.cursor()
        try:
            cur.executemany(query, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"error:{e}")
        cur.close()

    orden_id = '{{ dag_run.conf["id"] }}'
    df = extract(orden_id)
    df = transform(df)
    load_orden(df)
    load_products(df)

pipeline_etl = pipeline_etl()