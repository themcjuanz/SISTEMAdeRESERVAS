from Maleta import Maleta
from Maleta import tipoMaleta

class MaletaCabina(Maleta):
    def __init__(self, peso = 0.0):
        super().__init__(tipo=tipoMaleta.CABINA, peso=peso)

    def calcularPrecio(self):
        return 0.0
