import json
from typing import List

# Implementación concreta usando archivos .txt (JSON línea por línea)
class PersistenciaTXT:

    def cargar_usuarios(self, ruta_archivo: str) -> List[dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return [json.loads(linea) for linea in archivo]
        except FileNotFoundError:
            return []

    def guardar_usuarios(self, ruta_archivo: str, usuarios: List[dict]) -> None:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for usuario in usuarios:
                archivo.write(json.dumps(usuario) + "\n")

    def cargar_vuelos(self, ruta_archivo: str) -> List[dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return [json.loads(linea) for linea in archivo]
        except FileNotFoundError:
            return []

    def guardar_vuelos(self, ruta_archivo: str, vuelos: List[dict]) -> None:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for vuelo in vuelos:
                archivo.write(json.dumps(vuelo) + "\n")

    def cargar_reservas(self, ruta_archivo: str) -> List[dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return [json.loads(linea) for linea in archivo]
        except FileNotFoundError:
            return []

    def guardar_reservas(self, ruta_archivo: str, reservas: List[dict]) -> None:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for reserva in reservas:
                archivo.write(json.dumps(reserva) + "\n")

    # Método para cargar datos tabulados (admite separadores de tabulación o espacios)
    def cargar_vuelos_desde_archivo_tab(self, ruta_archivo: str) -> List[dict]:
        print(f"Cargando vuelos desde archivo tabulado: {ruta_archivo}")
        vuelos: List[dict] = []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for idx, linea in enumerate(archivo, start=1):
                    # Depuración: mostrar línea cruda
                    raw = linea.rstrip("\n")
                    print(f"Línea {idx}: '{raw}'")
                    # Separar en cualquier espacio en blanco (tabs o espacios múltiples)
                    partes = raw.split()
                    print(f"Partes obtenidas: {partes}")
                    if len(partes) == 7:
                        vuelo = {
                            'codigo': partes[0],
                            'origen': partes[1],
                            'destino': partes[2],
                            'dia': partes[3],
                            'hora': partes[4],
                            'sillas_preferencial': int(partes[5]),
                            'sillas_economica': int(partes[6])
                        }
                        vuelos.append(vuelo)
                    else:
                        print(f"Advertencia: línea {idx} no tiene 7 columnas, tiene {len(partes)}")
        except FileNotFoundError:
            print(f"Error: archivo {ruta_archivo} no encontrado.")
        print(f"Total vuelos cargados: {len(vuelos)}")
        return vuelos

if __name__ == '__main__':
    print("Entrando a main")
    archivo_tabulado = 'vuelos_tabulados.txt'
    archivo_json = 'vuelos.txt'

    persistencia = PersistenciaTXT()

    # Cargar datos tabulados y guardarlos en formato JSON línea por línea
    vuelos = persistencia.cargar_vuelos_desde_archivo_tab(archivo_tabulado)
    persistencia.guardar_vuelos(archivo_json, vuelos)

    print(f"Se han importado {len(vuelos)} vuelos y guardado en '{archivo_json}'")