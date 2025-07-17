from typing import List
from Usuario import Usuario
from Maleta import Maleta
from Vuelo import Vuelo

class Reserva:
    """
    Representa una reserva de vuelo, gestionando pasajeros, equipaje
    y cálculo de precios y millas.
    """

    def __init__(
        self,
        id: str,
        usuario: Usuario,
        vuelo: Vuelo,
        no_sillas: int,
        precio_base: float
    ):
        # Validaciones básicas
        if no_sillas <= 0:
            raise ValueError("El número de sillas debe ser mayor que cero.")
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")

        self.id = id
        self.usuario = usuario
        self.vuelo = vuelo
        self.no_sillas = no_sillas
        self.precio_base = precio_base
        self.pasajeros: List[Usuario] = []
        self.maletas: List[Maleta] = []
        self.checked_in = False

    def agregar_pasajero(self, pasajero: Usuario) -> None:
        """
        Agrega un objeto Usuario como pasajero adicional a la reserva.
        """
        self.pasajeros.append(pasajero)

    def _validar_maletas(self, maletas: List[Maleta]) -> None:
        """
        Valida que cada maleta cumpla criterios de peso y tipo.
        Se puede extender según políticas de la aerolínea.
        """
        for m in maletas:
            if m.peso <= 0:
                raise ValueError(f"Maleta con peso inválido: {m.peso}")

    def check_in(self, maletas: List[Maleta]) -> None:
        """
        Realiza el check-in, registrando equipaje y evitando dobles check-in.

        :param maletas: lista de instancias de Maleta para facturar
        :raises RuntimeError: si ya se había hecho check-in antes
        """
        if self.checked_in:
            raise RuntimeError("El check-in ya fue realizado previamente.")

        self._validar_maletas(maletas)
        self.maletas = list(maletas)
        self.checked_in = True

    def calcular_precio(self) -> float:
        """
        Calcula el precio total de la reserva incluyendo el equipaje.
        """
        total = self.precio_base * self.no_sillas
        for maleta in self.maletas:
            precio_maleta = maleta.calcularPrecio(maleta.peso)
            if precio_maleta is None:
                raise RuntimeError(f"Error calculando precio de maleta: {maleta}")
            total += precio_maleta
        return total

    def calcular_millas(self) -> int:
        """
        Devuelve las millas generadas por esta reserva, sin modificar el estado.
        """
        return 500 * self.no_sillas

    def acreditar_millas(self) -> int:
        """
        Suma las millas de esta reserva al usuario y retorna las acreditadas.
        """
        millas = self.calcular_millas()
        self.usuario.millas += millas
        return millas

    def resumen(self) -> dict:
        """
        Retorna un resumen puro de la reserva sin modificar estado:
        - id de reserva
        - id de usuario
        - código de vuelo
        - número de asientos
        - precio total
        - millas generadas (no acreditadas)
        """
        return {
            'id': self.id,
            'usuario_id': self.usuario.getId(),
            'vuelo_codigo': self.vuelo.getCodigo(),
            'no_sillas': self.no_sillas,
            'precio_total': self.calcular_precio(),
            'millas_generadas': self.calcular_millas()
        }
