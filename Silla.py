from abc import ABC, abstractmethod

class Silla(ABC):
    def __init__(self, id=0, tipo="", precio=0.0):
        self.id = id
        self.tipo = tipo
        self.precio = precio

    @abstractmethod
    def calcularPrecio(self): pass