from typing import List
from abc import ABC, abstractmethod

class Persistencia(ABC):
    @abstractmethod
    def cargar_usuarios(self, ruta_archivo: str) -> List[dict]: pass

    @abstractmethod
    def guardar_usuarios(self, ruta_archivo: str, usuarios: List[dict]) -> None: pass

    @abstractmethod
    def cargar_vuelos(self, ruta_archivo: str) -> List[dict]: pass

    @abstractmethod
    def guardar_vuelos(self, ruta_archivo: str, vuelos: List[dict]) -> None: pass

    @abstractmethod
    def cargar_reservas(self, ruta_archivo: str) -> List[dict]: pass

    @abstractmethod
    def guardar_reservas(self, ruta_archivo: str, reservas: List[dict]) -> None: pass

