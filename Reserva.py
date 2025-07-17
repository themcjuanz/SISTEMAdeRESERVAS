from typing import List
from Usuario import Usuario
from Maleta import Maleta
from Vuelo import Vuelo

class Reserva:
    def __init__(self, id: str, usuario: Usuario, vuelo: Vuelo, no_sillas: int, precio_base: float):
        self.id = id
        self.usuario = usuario       # Ahora es instancia de Usuario
        self.vuelo = vuelo           # Puede ser dict o clase Vuelo según tu diseño
        self.no_sillas = no_sillas
        self.pasajeros: List[Usuario] = []  # Lista de objetos Usuario como pasajeros adicionales
        self.maletas: List[Maleta] = []     # Lista de objetos Maleta (MaletaMano, MaletaCabina, MaletaBodega)
        self.precio_base = precio_base
        self.checked_in = False

    def agregar_pasajero(self, pasajero: Usuario) -> None:
        """
        Agrega un objeto Usuario como pasajero a la reserva.
        """
        self.pasajeros.append(pasajero)

    def check_in(self, maletas: List[Maleta]) -> None:
        """
        Registra el check-in y almacena la lista de Maleta.
        Convierte el tipo de cada Maleta a mayúsculas para consistencia.
        """
        if not self.checked_in:
            self.checked_in = True
            self.maletas = []
            for m in maletas:
                self.maletas.append(m)

    def calcular_precio(self) -> float:
        total = self.precio_base * self.no_sillas
        for maleta in self.maletas:
            precio_maleta = maleta.calcularPrecio(maleta.peso)
            if precio_maleta is not None:
                total += precio_maleta
        return total

    def calcular_millas(self) -> int:
        millas_reserva = 500 * self.no_sillas
        # Actualiza millas del usuario
        self.usuario.millas += millas_reserva
        return millas_reserva

    def resumen(self) -> dict:
        """
        Retorna un dict resumen de la reserva para mostrar o persistir.
        """
        return {
            'id': self.id,
            'usuario_id': self.usuario.getId(),
            'vuelo_codigo': self.vuelo.getCodigo(),
            'no_sillas': self.no_sillas,
            'precio_total': self.calcular_precio(),
            'millas_obtenidas': self.calcular_millas()
        }
