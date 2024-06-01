from abc import ABC, abstractmethod
from typing import List
from entities import Orden, OrdenEstado, Ordenes

class RepositoriosOrden(ABC):

    @abstractmethod
    def crear(self, Orden: Orden) -> Orden:
        pass

    @abstractmethod
    def actualizar(self, Orden: Orden) -> Orden:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def ordenes(self) -> List[Orden]:
        pass

class RepositoriosOrdenEstado(ABC):

    @abstractmethod
    def actualizar(self, orden: OrdenEstado) -> OrdenEstado:
        pass


