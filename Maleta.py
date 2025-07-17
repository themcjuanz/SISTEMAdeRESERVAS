from abc import ABC, abstractmethod
from enum import Enum

tipoMaleta = Enum('tipoMaleta', ['MANO', 'CABINA', 'BODEGA'])

class Maleta(ABC):
    def __init__(self, tipo=tipoMaleta.MANO, peso=0.0):
        self.tipo = tipo
        self.peso = peso
    
    @abstractmethod
    def calcularPrecio(self, tipo, peso): pass