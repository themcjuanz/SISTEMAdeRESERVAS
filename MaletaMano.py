from Maleta import Maleta
from Maleta import tipoMaleta

class MaletaMano(Maleta):
    def __init__(self, peso = 0.0):
        super().__init__(tipo=tipoMaleta.MANO, peso=peso)

    def calcularPrecio(self, tipo, peso):
        return 0.0
