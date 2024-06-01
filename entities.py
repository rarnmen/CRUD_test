from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class Orden:
    id: int = None
    ubicacion: str = None
    nombre_cliente: str = None
    nombre_operador: date = None
    productos: list = None
    #estado_id: int = None
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
