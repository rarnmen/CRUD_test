import psycopg2
from typing import List
from entities import Orden, OrdenEstado, Ordenes
from interfaces import RepositoriosOrden, RepositoriosOrdenEstado, RepositoriosOrdenes
import json
from dotenv import load_dotenv
import os

load_dotenv()
host = os.environ.get('HOST_POSTGRES')
database = os.environ.get('PASSWORD_POSTGRES')
user = os.environ.get('USER_POSTGRES')
password = os.environ.get('PASSWORD_POSTGRES')
port = os.environ.get('PORT_POSTGRES')

class Error():  
    def __init__(self, error: str = None) -> None:
        self.error=error

class RepositorioOrdenPostgres(RepositoriosOrden):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=5432
        )

    def crear(self, orden: Orden) -> Orden:
        cur = self.conn.cursor()
        query = "INSERT INTO raw_data.orden (ubicacion, nombre_cliente, nombre_operador, productos, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at"
        valores = (orden.ubicacion, orden.nombre_cliente, orden.nombre_operador, orden.productos, orden.created_at)
        try:
            cur.execute(query, valores)
            self.conn.commit()
            return_data = cur.fetchall() 
            print(return_data)      
            id_orden = return_data[0][0]
            created_at_orden = return_data[0][1]
            orden.id = id_orden
            orden.created_at = created_at_orden
        except Exception as e:
            self.conn.rollback()
            return Error(str(e))
        
        cur.close()
        return orden
    def actualizar(self, orden: Orden) -> Orden:
        cur = self.conn.cursor()
        query = """
            UPDATE raw_data.orden
            SET ubicacion = %s,
                nombre_cliente = %s,
                nombre_operador = %s,
                productos = %s,
                updated_at = NOW()
            WHERE id = %s
            RETURNING created_at, updated_at, delivered_at
        """
        valores = (orden.ubicacion, orden.nombre_cliente, orden.nombre_operador, orden.productos, orden.id)
        try:
            cur.execute(query, valores)
            self.conn.commit()
            created_at, updated_at, delivered_at = cur.fetchone()
            orden.created_at = created_at
            orden.updated_at = updated_at
            orden.delivered_at = delivered_at
        except Exception as e:
            self.conn.rollback()
            return Error(str(e))
        cur.close()
        return orden
    def eliminar(self, id: int) -> bool:
        cur = self.conn.cursor()
        query = "DELETE FROM raw_data.estado WHERE orden_id = %s; \
                 DELETE FROM raw_data.orden WHERE id = %s;"
        try:
            cur.execute(query, (id, id))
            self.conn.commit()
            eliminado = cur.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            eliminado = False
            print(f"error: {e}")
        cur.close()
        return eliminado
    
    def ordenes(self) -> List[Orden]:
        cur = self.conn.cursor()
        #query = "SELECT id, ubicacion, nombre_cliente, nombre_operador, productos, created_at, updated_at, delivered_at FROM orden"
        query = "SELECT * FROM raw_data.orden"

        try:
            cur.execute(query)
            rows = cur.fetchall()
            ordenes = []
            for row in rows:
                id, ubicacion, nombre_cliente, nombre_operador, productos_json, created_at, updated_at, delivered_at = row
                productos = json.loads(productos_json)
                orden = Orden(id, ubicacion, nombre_cliente, nombre_operador, productos, created_at, updated_at, delivered_at)
                ordenes.append(orden)
        except Exception as e:
            return Error(str(e))
        cur.close()
        return ordenes

class RepositorioOrdenEstadoPostgres(RepositoriosOrdenEstado):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=5432
        )

    def actualizar(self, orden_estado: OrdenEstado) -> OrdenEstado:
        cur = self.conn.cursor()
        query = "INSERT INTO raw_data.estado (orden_id, estado, tiempo_estado) VALUES (%s, %s, %s) RETURNING id, timestamp"
        valores = (orden_estado.orden_id, orden_estado.estado, orden_estado.tiempo_estado)
        try:
            cur.execute(query, valores)
            self.conn.commit()
            return_data = cur.fetchall()
            estado_id = return_data[0][0]
            estado_timestamp = return_data[0][1]
            orden_estado.id = estado_id
            orden_estado.timestamp = estado_timestamp
        except Exception as e:
            self.conn.rollback()
            return Error(str(e))
        cur.close()

        return orden_estado
        


