# CRUD_test
1. Aquí cree dos entitdades
llamadas Orden y OrdenEstado haciendo referencia al esquema raw_data en la base datos y las tablas orden y estado respectivamente.
```python
@dataclass
class Orden:
    id: int = None
    ubicacion: str = None
    nombre_cliente: str = None
    nombre_operador: date = None
    productos: list = None
    created_at: datetime = None
    updated_at: datetime = None
    delivered_at: datetime = None

@dataclass
class OrdenEstado:
    id: int = None
    orden_id: int = None
    estado: int = None
    tiempo_estado: str = None
    timestamp: datetime = None 

```
La lógica de la base de datos se describe la siguiente figura 

![](./doc/image/database.png)

Cuando un registro de una orden se realiza, se crea un estado asociado y esa registro pasa por un proceso de ETL para transformar los datos y cargar el base de datos summary_data. En esta ultima base de datos, hay dos tablas ordenes y productos donde se carga la data procesada.


![alt text](./doc/image/propose.png)
