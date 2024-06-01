from typing import List
from entities import Orden, OrdenEstado


 
class OrdenCasoUso:
    def __init__(self, repo_orden):
        self.repo_orden = repo_orden

    def crear_orden(self, orden: Orden)-> Orden:
        return self.repo_orden.crear(orden)
    def eliminar_orden(self, id: int)-> bool:
        return self.repo_orden.eliminar(id)
    
    def actualizar_orden(self, orden: Orden)-> Orden:
        return self.repo_orden.actualizar(orden)
    
    def ordenes(self)-> List[Orden]:
        return self.repo_orden.ordenes()

class EstadoCasoUso:
    def __init__(self, repo_estado):
        self.repo_estado = repo_estado
    
    def actualizar_estado(self, orden_estado: OrdenEstado)-> OrdenEstado:
        return self.repo_estado.actualizar(orden_estado)