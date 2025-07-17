from datetime import date

class Vuelo:
    def __init__(self, codigo: str, origen: str, destino: str, horario: date, sillasEconomicas: int, sillasPrefenciales: int):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.horario = horario
        self.sillasEconomicas= sillasEconomicas
        self.sillasPrefenciales = sillasPrefenciales

        def getCodigo(self):
            return self.codigo

        def verificarDisponibilidad(self, cantidad: int, tipoSilla: str):
            pass
        def reservarSillas(self, cantidad: int, tipoSilla: str):
            pass
        def liberarSillas(self, cantidad: int, tipoSilla: str):
            pass
