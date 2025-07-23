import json
from typing import List, Dict

class PersistenciaTXT:
    def cargar_usuarios(self, ruta_archivo: str) -> List[Dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return [json.loads(linea) for linea in archivo]
        except FileNotFoundError:
            return []

    def guardar_usuarios(self, ruta_archivo: str, usuarios: List[Dict]) -> None:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for u in usuarios:
                archivo.write(json.dumps(u, ensure_ascii=False) + "\n")

    def cargar_vuelos(self, ruta_archivo: str) -> List[Dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return [json.loads(linea) for linea in archivo]
        except FileNotFoundError:
            return []

    def guardar_vuelos(self, ruta_archivo: str, vuelos: List[Dict], append: bool = False) -> None:
        """
        Exporta vuelos en formato pipe-separated (|) a partir de listas de dict:
        codigo|origen|destino|dia|hora|sillas_preferencial|sillas_economica
        """
        modo = "a" if append else "w"
        with open(ruta_archivo, modo, encoding="utf-8") as archivo:
            for v in vuelos:
                linea = (
                    f"{v['codigo']}|{v['origen']}|{v['destino']}|"
                    f"{v['dia']}|{v['hora']}|{v['sillas_preferencial']}|{v['sillas_economica']}"
                )
                archivo.write(linea + "\n")

    def cargar_reservas(self, ruta_archivo: str) -> List[Dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return [json.loads(linea) for linea in archivo]
        except FileNotFoundError:
            return []

    def guardar_reservas(self, ruta_archivo: str, reservas: List[Dict]) -> None:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for r in reservas:
                archivo.write(json.dumps(r, ensure_ascii=False) + "\n")

    def cargar_vuelos_desde_archivo_tab(self, ruta_archivo: str) -> List[Dict]:
        """
        Carga vuelos desde un archivo tabulado (separador: '\t').
        Cada línea: codigo, origen, destino, dia, hora, sillas_preferencial, sillas_economica
        """
        vuelos: List[Dict] = []
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for idx, linea in enumerate(archivo, start=1):
                    partes = linea.rstrip('\n').split('\t')
                    if len(partes) != 7:
                        print(f"Advertencia: línea {idx} no tiene 7 columnas, tiene {len(partes)}")
                        continue
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
        except FileNotFoundError:
            print(f"Error: archivo '{ruta_archivo}' no encontrado.")
        return vuelos

# Ejemplo de uso sencillo:
if __name__ == '__main__':
    persistencia = PersistenciaTXT()
    # Carga desde tabulado:
    vuelos_tab = persistencia.cargar_vuelos_desde_archivo_tab('vuelos_tabulados.txt')
    print(f"Cargados {len(vuelos_tab)} vuelos desde tabulado.")
    # Exporta con '|' al archivo:
    persistencia.guardar_vuelos('vuelos_exportados.txt', vuelos_tab, append=False)
    print("Vuelos exportados con '|' como separador.")
