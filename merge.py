import os
import hashlib
class Usuario:
    def __init__(self, nombre, id_documento, email, contraseña, millas=0):
        self.nombre = nombre
        self.id_documento = id_documento
        self.email = email
        self.contraseña = self._hash_password(contraseña)
        self.millas = millas
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_contraseña(self, contraseña):
        return self.contraseña == self._hash_password(contraseña)
    
    def cambiar_contraseña(self, nueva_contraseña):
        self.contraseña = self._hash_password(nueva_contraseña)
    
    def agregar_millas(self, cantidad):
        self.millas += cantidad
    
    def usar_millas(self, cantidad):
        if self.millas >= cantidad:
            self.millas -= cantidad
            return True
        return False
    
    def getNombre(self):
        return self.nombre
    
    def to_string(self):
        return f"{self.nombre}|{self.id_documento}|{self.email}|{self.contraseña}|{self.millas}"
    
    @classmethod
    def from_string(cls, data):
        parts = data.strip().split('|')
        usuario = cls.__new__(cls)
        usuario.nombre = parts[0]
        usuario.id_documento = parts[1]
        usuario.email = parts[2]
        usuario.contraseña = parts[3]
        usuario.millas = int(parts[4])
        return usuario

class Vuelo:
    def __init__(self, codigo, origen, destino, hora,dia, sillas_preferencial, sillas_economica):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.hora = hora
        self.dia = dia
        self.sillas_preferencial_total = sillas_preferencial
        self.sillas_economica_total = sillas_economica
        self.sillas_preferencial_disponibles = sillas_preferencial
        self.sillas_economica_disponibles = sillas_economica
    
    def getCodigo(self):
        return self.codigo
    
    def getOrigen(self):
        return self.origen
    
    def getDestino(self):
        return self.destino
    
    def getHora(self):
        return self.hora
    
    def getDia(self):
        return self.dia
    
    def getSillasDisponibles(self, tipo):
        if tipo == 'PREFERENCIAL':
            return self.sillas_preferencial_disponibles
        else:
            return self.sillas_economica_disponibles
    
    def verificarDisponibilidad(self, cantidad, tipo):
        if tipo == 'PREFERENCIAL':
            return self.sillas_preferencial_disponibles >= cantidad
        else:
            return self.sillas_economica_disponibles >= cantidad
    
    def reservar_sillas(self, cantidad, tipo):
        if self.verificarDisponibilidad(cantidad, tipo):
            if tipo == 'PREFERENCIAL':
                self.sillas_preferencial_disponibles -= cantidad
            else:
                self.sillas_economica_disponibles -= cantidad
            return True
        return False
    
    def liberar_sillas(self, cantidad, tipo):
        if tipo == 'PREFERENCIAL':
            self.sillas_preferencial_disponibles = min(
                self.sillas_preferencial_disponibles + cantidad,
                self.sillas_preferencial_total
            )
        else:
            self.sillas_economica_disponibles = min(
                self.sillas_economica_disponibles + cantidad,
                self.sillas_economica_total
            )
    
    def to_string(self):
        return f"{self.codigo}|{self.origen}|{self.destino}|{self.hora}|{self.dia}|{self.sillas_preferencial_total}|{self.sillas_economica_total}|{self.sillas_preferencial_disponibles}|{self.sillas_economica_disponibles}"
    
    @classmethod
    def from_string(cls, data):
        parts = data.strip().split('|')
        print(f"Parsing vuelo from parts: {parts}")
        vuelo = cls(parts[0], parts[1], parts[2], parts[3], parts[4], int(parts[5]), int(parts[6]))
        vuelo.sillas_preferencial_disponibles = int(parts[5])
        vuelo.sillas_economica_disponibles = int(parts[6])
        return vuelo

class Pasajero:
    def __init__(self, nombre, id_documento, email=""):
        self.nombre = nombre
        self.id_documento = id_documento
        self.email = email

class Equipaje:
    def __init__(self):
        self.equipaje_mano = True  # Siempre incluido
        self.maleta_cabina = False
        self.maletas_bodega = 0
        self.peso_total = 0.0  # Cambiado a float
        self.costo_adicional = 0
    
    def calcular_costo(self, tipo_silla):
        costo = 0
        
        # Maleta de cabina
        if self.maleta_cabina and tipo_silla == 'ECONOMICA':
            costo += 40000
        
        # Maletas de bodega adicionales
        if tipo_silla == 'PREFERENCIAL':
            # 1 maleta incluida, adicionales tienen costo
            if self.maletas_bodega > 1:
                costo += (self.maletas_bodega - 1) * self.peso_total * 2000  # $2000 por kg adicional
        else:
            # Económica: todas las maletas tienen costo
            costo += self.maletas_bodega * self.peso_total * 2000
        
        return costo

class Reserva:
    contador_id = 1
    
    def __init__(self, usuario, vuelo, no_sillas, tipo_silla, pasajeros):
        self.id = f"R{Reserva.contador_id:04d}"
        Reserva.contador_id += 1
        self.usuario = usuario
        self.vuelo = vuelo
        self.no_sillas = no_sillas
        self.tipo_silla = tipo_silla
        self.pasajeros = pasajeros
        self.estado = "ACTIVA"
        self.check_in_realizado = False
        self.equipajes = []
        self.descuento_millas = False
    
    def calcular_precio(self):
        if self.tipo_silla == 'PREFERENCIAL':
            precio_base = 850000 if not self.descuento_millas else 235000
        else:
            precio_base = 235000
        
        precio_total = precio_base * self.no_sillas
        
        # Agregar costos de equipaje
        for equipaje in self.equipajes:
            precio_total += equipaje.calcular_costo(self.tipo_silla)
        
        return precio_total
    
    def realizar_check_in(self):
        if not self.check_in_realizado:
            self.check_in_realizado = True
            self.usuario.agregar_millas(500)  # 500 millas por reserva
            return True
        return False
    
    def cancelar(self):
        if self.estado == "ACTIVA":
            self.estado = "CANCELADA"
            self.vuelo.liberar_sillas(self.no_sillas, self.tipo_silla)
            return True
        return False
    
    def to_string(self):
        pasajeros_str = ";".join([f"{p['nombre']}:{p['id']}:{p['email']}" for p in self.pasajeros])
        return f"{self.id}|{self.usuario.id_documento}|{self.vuelo.codigo}|{self.no_sillas}|{self.tipo_silla}|{pasajeros_str}|{self.estado}|{self.check_in_realizado}|{self.descuento_millas}"
    
    @classmethod
    def from_string(cls, data, usuarios, vuelos):
        parts = data.strip().split('|')
        usuario = next((u for u in usuarios.values() if u.id_documento == parts[1]), None)
        vuelo = vuelos.get(parts[2])
        
        if not usuario or not vuelo:
            return None
        
        pasajeros_data = parts[5].split(';')
        pasajeros = []
        for p_data in pasajeros_data:
            if p_data:
                p_parts = p_data.split(':')
                pasajeros.append({
                    'nombre': p_parts[0],
                    'id': p_parts[1],
                    'email': p_parts[2] if len(p_parts) > 2 else ""
                })
        
        reserva = cls.__new__(cls)
        reserva.id = parts[0]
        reserva.usuario = usuario
        reserva.vuelo = vuelo
        reserva.no_sillas = int(parts[3])
        reserva.tipo_silla = parts[4]
        reserva.pasajeros = pasajeros
        reserva.estado = parts[6]
        reserva.check_in_realizado = parts[7] == 'True'
        reserva.descuento_millas = parts[8] == 'True' if len(parts) > 8 else False
        reserva.equipajes = []
        
        return reserva

class SistemaReservas:
    def __init__(self):
        self.usuarios = {}
        self.vuelos = {}
        self.reservas = {}
        self.usuario_actual = None
        self.admin_password = "admin123"
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga datos desde archivos"""
        try:
            # Cargar usuarios
            if os.path.exists("usuarios.txt"):
                with open("usuarios.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            usuario = Usuario.from_string(line)
                            self.usuarios[usuario.id_documento] = usuario
            
            # Cargar vuelos
            if os.path.exists("vuelos_exportados.txt"):
                with open("vuelos_exportados.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            vuelo = Vuelo.from_string(line)
                            self.vuelos[vuelo.codigo] = vuelo
            
            # Cargar reservas
            if os.path.exists("reservas.txt"):
                with open("reservas.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            reserva = Reserva.from_string(line, self.usuarios, self.vuelos)
                            if reserva:
                                self.reservas[reserva.id] = reserva
                                # Actualizar contador
                                num = int(reserva.id[1:])
                                if num >= Reserva.contador_id:
                                    Reserva.contador_id = num + 1
        
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def guardar_datos(self):
        """Guarda datos en archivos"""
        try:
            # Guardar usuarios
            with open("usuarios.txt", "w", encoding="utf-8") as f:
                for usuario in self.usuarios.values():
                    f.write(usuario.to_string() + "\n")
            
            # Guardar vuelos
            file_path = "vuelos_tabulados.txt"
            first_write = not os.path.exists(file_path) or os.path.getsize(file_path) == 0

            with open(file_path, "a", encoding="utf-8") as f:
                if first_write:
                    f.write("CÓDIGO|ORIGEN|DESTINO|HORA|DIA|PREF|ECON\n")
                for vuelo in self.vuelos.values():
                    f.write(vuelo.to_string() + "\n")
            
            # Guardar reservas
            with open("reservas.txt", "w", encoding="utf-8") as f:
                for reserva in self.reservas.values():
                    f.write(reserva.to_string() + "\n")
        
        except Exception as e:
            print(f"Error al guardar datos: {e}")
    
    def registrar_usuario(self, nombre, id_documento, email, contraseña):
        """Registra un nuevo usuario"""
        if id_documento in self.usuarios:
            return False
        
        usuario = Usuario(nombre, id_documento, email, contraseña)
        self.usuarios[id_documento] = usuario
        self.guardar_datos()
        return True
    
    def iniciar_sesion(self, id_documento, contraseña):
        """Inicia sesión de usuario"""
        if id_documento in self.usuarios:
            usuario = self.usuarios[id_documento]
            if usuario.verificar_contraseña(contraseña):
                self.usuario_actual = usuario
                return True
        return False
    
    def verificar_admin(self, contraseña):
        """Verifica credenciales de administrador"""
        return contraseña == self.admin_password
    
    def buscar_vuelos(self, origen=None, destino=None):
        """Busca vuelos por origen y/o destino"""
        vuelos_encontrados = []
        for vuelo in self.vuelos.values():
            if origen and vuelo.origen.lower() != origen.lower():
                continue
            if destino and vuelo.destino.lower() != destino.lower():
                continue
            vuelos_encontrados.append(vuelo)
        return vuelos_encontrados
    
    def crear_reserva(self, codigo_vuelo, cantidad, tipo_silla, pasajeros, usar_descuento_millas=False):
        """Crea una nueva reserva"""
        if not self.usuario_actual or codigo_vuelo not in self.vuelos:
            return None
        
        vuelo = self.vuelos[codigo_vuelo]
        
        if not vuelo.verificarDisponibilidad(cantidad, tipo_silla):
            return None
        
        # Verificar descuento por millas
        if usar_descuento_millas and tipo_silla == 'PREFERENCIAL':
            if not self.usuario_actual.usar_millas(2000):
                return None
        
        # Reservar sillas
        vuelo.reservar_sillas(cantidad, tipo_silla)
        
        # Crear reserva
        reserva = Reserva(self.usuario_actual, vuelo, cantidad, tipo_silla, pasajeros)
        reserva.descuento_millas = usar_descuento_millas
        
        self.reservas[reserva.id] = reserva
        self.guardar_datos()
        
        return reserva.id
    
    def obtener_reservas_usuario(self):
        """Obtiene las reservas del usuario actual"""
        if not self.usuario_actual:
            return []
        
        return [r for r in self.reservas.values() 
                if r.usuario.id_documento == self.usuario_actual.id_documento 
                and r.estado == "ACTIVA"]
    
    def agregar_vuelo(self, codigo, origen, destino, hora,dia, sillas_pref, sillas_eco):
        """Agrega un nuevo vuelo (admin)"""
        if codigo in self.vuelos:
            return False

        vuelo = Vuelo(codigo, origen, destino, hora, dia, sillas_pref, sillas_eco)
        self.vuelos[codigo] = vuelo
        self.guardar_datos()
        return True
    
    def modificar_vuelo(self, codigo, **kwargs):
        """Modifica un vuelo existente (admin)"""
        if codigo not in self.vuelos:
            return False
        
        vuelo = self.vuelos[codigo]
        for key, value in kwargs.items():
            if hasattr(vuelo, key):
                setattr(vuelo, key, value)
        
        self.guardar_datos()
        return True
    
    def consultar_ventas(self):
        """Consulta ventas por vuelo (admin)"""
        ventas = {}
        for reserva in self.reservas.values():
            if reserva.estado == "ACTIVA":
                codigo = reserva.vuelo.codigo
                if codigo not in ventas:
                    ventas[codigo] = {
                        'vuelo': reserva.vuelo,
                        'sillas_vendidas': 0,
                        'ingresos': 0,
                        'pasajeros': []
                    }
                
                ventas[codigo]['sillas_vendidas'] += reserva.no_sillas
                ventas[codigo]['ingresos'] += reserva.calcular_precio()
                ventas[codigo]['pasajeros'].extend(reserva.pasajeros)
        
        return ventas

# Funciones de interfaz (continuación del código original)

def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*50)
    print("    SISTEMA DE RESERVAS DE VUELOS")
    print("="*50)
    print("1. Registrarse")
    print("2. Iniciar Sesión")
    print("3. Acceso Administrador")
    print("4. Salir")
    print("="*50)

def mostrar_menu_usuario():
    """Muestra el menú para usuarios autenticados"""
    print("\n" + "="*50)
    print("    MENÚ USUARIO")
    print("="*50)
    print("1. Buscar Vuelos")
    print("2. Realizar Reserva")
    print("3. Mis Reservas")
    print("4. Check-in")
    print("5. Cambiar Contraseña")
    print("6. Cerrar Sesión")
    print("="*50)

def mostrar_menu_admin():
    """Muestra el menú para administradores"""
    print("\n" + "="*50)
    print("    MENÚ ADMINISTRADOR")
    print("="*50)
    print("1. Agregar Vuelo")
    print("2. Modificar Vuelo")
    print("3. Consultar Ventas")
    print("4. Ver Todos los Vuelos")
    print("5. Volver al Menú Principal")
    print("="*50)

def registrar_usuario(sistema):
    """Maneja el registro de nuevos usuarios"""
    print("\n--- REGISTRO DE USUARIO ---")
    nombre = input("Nombre completo: ").strip()
    id_doc = input("Número de documento: ").strip()
    email = input("Correo electrónico: ").strip()
    
    while True:
        contraseña = input("Contraseña: ").strip()
        confirmar = input("Confirmar contraseña: ").strip()
        if contraseña == confirmar:
            break
        print("Las contraseñas no coinciden. Intente de nuevo.")
    
    if sistema.registrar_usuario(nombre, id_doc, email, contraseña):
        print("✓ Usuario registrado exitosamente!")
    else:
        print("✗ Error: El usuario ya existe.")

def iniciar_sesion(sistema):
    """Maneja el inicio de sesión"""
    print("\n--- INICIAR SESIÓN ---")
    id_doc = input("Número de documento: ").strip()
    contraseña = input("Contraseña: ").strip()
    
    if sistema.iniciar_sesion(id_doc, contraseña):
        print(f"✓ Bienvenido, {sistema.usuario_actual.getNombre()}!")
        print(f"Millas acumuladas: {sistema.usuario_actual.millas}")
        return True
    else:
        print("✗ Credenciales incorrectas.")
        return False

def acceso_admin(sistema):
    """Maneja el acceso de administrador"""
    print("\n--- ACCESO ADMINISTRADOR ---")
    contraseña = input("Contraseña de administrador: ").strip()
    
    if sistema.verificar_admin(contraseña):
        print("✓ Acceso autorizado!")
        return True
    else:
        print("✗ Contraseña incorrecta.")
        return False

def buscar_vuelos(sistema):
    """Permite buscar vuelos"""
    print("\n--- BUSCAR VUELOS ---")
    origen = input("Ciudad de origen (Enter para omitir): ").strip()
    destino = input("Ciudad de destino (Enter para omitir): ").strip()
    
    vuelos = sistema.buscar_vuelos(
        origen if origen else None,
        destino if destino else None
    )
    
    if not vuelos:
        print("No se encontraron vuelos con esos criterios.")
        return
    
    print("\n--- VUELOS DISPONIBLES ---")
    print(f"{'Código':<8} {'Origen':<12} {'Destino':<12} {'Horario':<16} {'Eco.':<6} {'Pref.':<6}")
    print("-" * 70)
    
    for vuelo in vuelos:
        eco_disp = vuelo.getSillasDisponibles('ECONOMICA')
        pref_disp = vuelo.getSillasDisponibles('PREFERENCIAL')
        print(f"{vuelo.getCodigo():<8} {vuelo.getOrigen():<12} {vuelo.getDestino():<12} "
              f"{str(vuelo.getHora()):<16}{vuelo.getDia():<12} {eco_disp:<6} {pref_disp:<6}")

def realizar_reserva(sistema):
    """Maneja la creación de reservas"""
    print("\n--- REALIZAR RESERVA ---")
    
    # Mostrar vuelos disponibles primero
    buscar_vuelos(sistema)
    
    codigo_vuelo = input("\nCódigo del vuelo: ").strip().upper()
    
    if codigo_vuelo not in sistema.vuelos:
        print("✗ Vuelo no encontrado.")
        return
    
    vuelo = sistema.vuelos[codigo_vuelo]
    
    try:
        cantidad = int(input("Cantidad de sillas (máx. 3): "))
        if cantidad < 1 or cantidad > 3:
            print("✗ Cantidad inválida. Debe ser entre 1 y 3.")
            return
    except ValueError:
        print("✗ Cantidad inválida.")
        return
    
    print("\nTipos de silla disponibles:")
    print("1. Económica ($235.000)")
    print("2. Preferencial ($850.000)")
    
    usar_descuento = False
    # Verificar descuento por millas
    if sistema.usuario_actual.millas >= 2000:
        print("3. Preferencial con descuento por millas ($235.000)")
    
    try:
        opcion = int(input("Seleccione tipo de silla: "))
        if opcion == 1:
            tipo_silla = 'ECONOMICA'
        elif opcion == 2:
            tipo_silla = 'PREFERENCIAL'
        elif opcion == 3 and sistema.usuario_actual.millas >= 2000:
            tipo_silla = 'PREFERENCIAL'
            usar_descuento = True
        else:
            print("✗ Opción inválida.")
            return
    except ValueError:
        print("✗ Opción inválida.")
        return
    
    # Verificar disponibilidad
    if not vuelo.verificarDisponibilidad(cantidad, tipo_silla):
        print("✗ No hay suficientes sillas disponibles.")
        return
    
    # Recopilar información de pasajeros
    pasajeros = []
    for i in range(cantidad):
        print(f"\n--- PASAJERO {i+1} ---")
        nombre = input("Nombre completo: ").strip()
        id_pasajero = input("Número de documento: ").strip()
        email = input("Email (opcional): ").strip()
        
        pasajeros.append({
            'nombre': nombre,
            'id': id_pasajero,
            'email': email
        })
    
    # Calcular y mostrar resumen
    if tipo_silla == 'PREFERENCIAL':
        precio_por_silla = 850000 if not usar_descuento else 235000
    else:
        precio_por_silla = 235000
    
    total = precio_por_silla * cantidad
    
    print("\n--- RESUMEN DE COMPRA ---")
    print(f"Vuelo: {codigo_vuelo}")
    print(f"Ruta: {vuelo.getOrigen()} → {vuelo.getDestino()}")
    print(f"Hora: {vuelo.getHora()}")
    print(f"Dia: {vuelo.getDia()}")
    print(f"Tipo de silla: {tipo_silla}")
    print(f"Cantidad: {cantidad}")
    print(f"Precio por silla: ${precio_por_silla:,}")
    print(f"TOTAL: ${total:,}")
    
    if usar_descuento:
        print("Se descontarán 2000 millas de su cuenta.")
    
    confirmar = input("\n¿Confirmar reserva? (s/n): ").strip().lower()
    if confirmar == 's':
        try:
            id_reserva = sistema.crear_reserva(codigo_vuelo, cantidad, tipo_silla, pasajeros, usar_descuento)
            if id_reserva:
                print(f"✓ Reserva creada exitosamente!")
                print(f"Número de reserva: {id_reserva}")
            else:
                print("✗ Error al crear la reserva.")
        except Exception as e:
            print(f"✗ Error: {e}")

def mostrar_reservas(sistema):
    """Muestra las reservas del usuario actual"""
    reservas = sistema.obtener_reservas_usuario()
    
    if not reservas:
        print("No tienes reservas activas.")
        return reservas
    
    print("\n--- MIS RESERVAS ---")
    for i, reserva in enumerate(reservas, 1):
        print(f"\n{i}. Reserva ID: {reserva.id}")
        print(f"   Vuelo: {reserva.vuelo.getCodigo()}")
        print(f"   Ruta: {reserva.vuelo.getOrigen()} → {reserva.vuelo.getDestino()}")
        print(f"   Hora: {reserva.vuelo.getHora()}")
        print(f"   Fecha: {reserva.vuelo.getDia()}")
        print(f"   Tipo: {reserva.tipo_silla}")
        print(f"   Sillas: {reserva.no_sillas}")
        print(f"   Precio total: ${reserva.calcular_precio():,}")
        print(f"   Check-in: {'✓ Realizado' if reserva.check_in_realizado else '✗ Pendiente'}")
        
        print("   Pasajeros:")
        for j, pasajero in enumerate(reserva.pasajeros, 1):
            print(f"     {j}. {pasajero['nombre']} - {pasajero['id']}")
    
    return reservas

def gestionar_reservas(sistema):
    """Permite gestionar reservas existentes"""
    reservas = mostrar_reservas(sistema)
    
    if not reservas:
        return
    
    print("\n--- GESTIÓN DE RESERVAS ---")
    print("1. Cancelar reserva")
    print("2. Volver al menú")
    
    try:
        opcion = int(input("Seleccione una opción: "))
        if opcion == 1:
            try:
                num_reserva = int(input("Número de reserva a cancelar: "))
                if 1 <= num_reserva <= len(reservas):
                    reserva = reservas[num_reserva - 1]
                    confirmar = input(f"¿Confirmar cancelación de reserva {reserva.id}? (s/n): ").strip().lower()
                    if confirmar == 's':
                        if reserva.cancelar():
                            sistema.guardar_datos()
                            print("✓ Reserva cancelada exitosamente.")
                        else:
                            print("✗ Error al cancelar la reserva.")
                    else:
                        print("Cancelación abortada.")
                else:
                    print("✗ Número de reserva inválido.")
            except ValueError:
                print("✗ Número inválido.")
    except ValueError:
        print("✗ Opción inválida.")

def realizar_check_in(sistema):
    """Maneja el proceso de check-in"""
    reservas = [r for r in sistema.obtener_reservas_usuario() if not r.check_in_realizado]
    
    if not reservas:
        print("No tienes reservas pendientes de check-in.")
        return
    
    print("\n--- CHECK-IN ---")
    print("Reservas disponibles para check-in:")
    
    for i, reserva in enumerate(reservas, 1):
        print(f"{i}. Reserva {reserva.id} - Vuelo {reserva.vuelo.getCodigo()}")
        print(f"   Ruta: {reserva.vuelo.getOrigen()} → {reserva.vuelo.getDestino()}")
        print(f"   Hora: {reserva.vuelo.getHora()}-{reserva.vuelo.getDia()}")
    
    try:
        num_reserva = int(input("Seleccione reserva para check-in: "))
        if 1 <= num_reserva <= len(reservas):
            reserva = reservas[num_reserva - 1]
            
            print(f"\n--- CHECK-IN RESERVA {reserva.id} ---")
            print(f"Vuelo: {reserva.vuelo.getCodigo()}")
            print(f"Ruta: {reserva.vuelo.getOrigen()} → {reserva.vuelo.getDestino()}")
            print(f"Hora: {reserva.vuelo.getHora()}")
            print(f"Dia: {reserva.vuelo.getDia()}")
            print(f"Pasajeros: {reserva.no_sillas}")
            print(f"Tipo de silla: {reserva.tipo_silla}")
            
            # Configurar equipaje
            print("\n--- SELECCIÓN DE EQUIPAJE ---")
            for i, pasajero in enumerate(reserva.pasajeros, 1):
                print(f"\nPasajero {i}: {pasajero['nombre']}")
                equipaje = Equipaje()
                
                print("Equipaje de mano: ✓ Incluido")
                
                # Maleta de cabina
                if reserva.tipo_silla == 'PREFERENCIAL':
                    print("Maleta de cabina (10kg): ✓ Incluida")
                    equipaje.maleta_cabina = True
                else:
                    maleta_cabina = input("¿Agregar maleta de cabina ($40.000)? (s/n): ").strip().lower()
                    if maleta_cabina == 's':
                        equipaje.maleta_cabina = True
                
                # Maletas de bodega
                try:
                    if reserva.tipo_silla == 'PREFERENCIAL':
                        print("Maleta de bodega: ✓ 1 incluida")
                        adicionales = int(input("Maletas adicionales de bodega (0 para ninguna): "))
                        equipaje.maletas_bodega = 1 + adicionales
                        if adicionales > 0:
                            equipaje.peso_total = float(input("Peso total de maletas adicionales (kg): "))
                    else:
                        equipaje.maletas_bodega = int(input("Número de maletas de bodega (0 para ninguna): "))
                        if equipaje.maletas_bodega > 0:
                            equipaje.peso_total = float(input("Peso total de las maletas (kg): "))
                except ValueError:
                    print("Valor inválido, usando configuración por defecto.")
                    equipaje.maletas_bodega = 1 if reserva.tipo_silla == 'PREFERENCIAL' else 0
                
                reserva.equipajes.append(equipaje)
            
            # Mostrar resumen final y confirmar check-in
            precio_inicial = reserva.calcular_precio()
            costo_equipaje = sum(eq.calcular_costo(reserva.tipo_silla) for eq in reserva.equipajes)
            
            print(f"\n--- RESUMEN FINAL ---")
            print(f"Precio base de la reserva: ${precio_inicial - costo_equipaje:,}")
            if costo_equipaje > 0:
                print(f"Costo adicional por equipaje: ${costo_equipaje:,}")
                print(f"TOTAL A PAGAR: ${precio_inicial:,}")
            else:
                print(f"TOTAL: ${precio_inicial:,}")
            
            confirmar = input("\n¿Confirmar check-in? (s/n): ").strip().lower()
            if confirmar == 's':
                if reserva.realizar_check_in():
                    sistema.guardar_datos()
                    print("✓ Check-in realizado exitosamente!")
                    print("Has ganado 500 millas por esta reserva.")
                    print(f"Millas totales: {sistema.usuario_actual.millas}")
                else:
                    print("✗ Error al realizar check-in.")
        else:
            print("✗ Número de reserva inválido.")
    except ValueError:
        print("✗ Entrada inválida.")

def cambiar_contraseña(sistema):
    """Permite cambiar la contraseña del usuario actual"""
    print("\n--- CAMBIAR CONTRASEÑA ---")
    
    contraseña_actual = input("Contraseña actual: ").strip()
    if not sistema.usuario_actual.verificar_contraseña(contraseña_actual):
        print("✗ Contraseña actual incorrecta.")
        return
    
    while True:
        nueva_contraseña = input("Nueva contraseña: ").strip()
        confirmar = input("Confirmar nueva contraseña: ").strip()
        if nueva_contraseña == confirmar:
            sistema.usuario_actual.cambiar_contraseña(nueva_contraseña)
            sistema.guardar_datos()
            print("✓ Contraseña cambiada exitosamente!")
            break
        print("Las contraseñas no coinciden. Intente de nuevo.")

# Funciones de administrador

def agregar_vuelo_admin(sistema):
    """Permite al admin agregar un nuevo vuelo"""
    print("\n--- AGREGAR VUELO ---")
    
    codigo = input("Código del vuelo: ").strip().upper()
    origen = input("Ciudad de origen: ").strip()
    destino = input("Ciudad de destino: ").strip()
    dia = input("Día (LUNES, MARTES,.., DOMINGO): ").strip()
    hora = input("Hora (ej: 08:30): ").strip()
    
    try:
        sillas_pref = int(input("Número de sillas preferenciales: "))
        sillas_eco = int(input("Número de sillas económicas: "))
        
        if sistema.agregar_vuelo(codigo, origen, destino,dia, hora, sillas_pref, sillas_eco):
            print("✓ Vuelo agregado exitosamente!")
        else:
            print("✗ Error: El vuelo ya existe.")
    except ValueError:
        print("✗ Número de sillas inválido.")

def modificar_vuelo_admin(sistema):
    """Permite al admin modificar un vuelo existente"""
    print("\n--- MODIFICAR VUELO ---")
    
    # Mostrar vuelos disponibles
    if not sistema.vuelos:
        print("No hay vuelos registrados.")
        return
    
    print("\nVuelos disponibles:")
    for vuelo in sistema.vuelos.values():
        print(f"{vuelo.getCodigo()}: {vuelo.getOrigen()} → {vuelo.getDestino()}")
    
    codigo = input("\nCódigo del vuelo a modificar: ").strip().upper()
    
    if codigo not in sistema.vuelos:
        print("✗ Vuelo no encontrado.")
        return
    
    vuelo = sistema.vuelos[codigo]
    print(f"\nVuelo actual: {vuelo.getOrigen()} → {vuelo.getDestino()}")
    print(f"Hora: {vuelo.getHora()}")
    print(f"Dia: {vuelo.getDia()}")
    print(f"Sillas preferenciales: {vuelo.sillas_preferencial_total}")
    print(f"Sillas económicas: {vuelo.sillas_economica_total}")
    
    print("\n¿Qué desea modificar?")
    print("1. Origen")
    print("2. Destino") 
    print("3. Horario")
    print("4. Sillas preferenciales")
    print("5. Sillas económicas")
    print("6. Cancelar")
    
    try:
        opcion = int(input("Seleccione opción: "))
        
        if opcion == 1:
            nuevo_origen = input("Nuevo origen: ").strip()
            sistema.modificar_vuelo(codigo, origen=nuevo_origen)
            print("✓ Origen modificado.")
        elif opcion == 2:
            nuevo_destino = input("Nuevo destino: ").strip()
            sistema.modificar_vuelo(codigo, destino=nuevo_destino)
            print("✓ Destino modificado.")
        elif opcion == 3:
            nuevo_horario = input("Nuevo horario: ").strip()
            sistema.modificar_vuelo(codigo, horario=nuevo_horario)
            print("✓ Horario modificado.")
        elif opcion == 4:
            nuevas_sillas = int(input("Nuevo número de sillas preferenciales: "))
            sistema.modificar_vuelo(codigo, sillas_preferencial_total=nuevas_sillas)
            print("✓ Sillas preferenciales modificadas.")
        elif opcion == 5:
            nuevas_sillas = int(input("Nuevo número de sillas económicas: "))
            sistema.modificar_vuelo(codigo, sillas_economica_total=nuevas_sillas)
            print("✓ Sillas económicas modificadas.")
        elif opcion == 6:
            print("Modificación cancelada.")
        else:
            print("✗ Opción inválida.")
    except ValueError:
        print("✗ Entrada inválida.")

def consultar_ventas_admin(sistema):
    """Muestra el reporte de ventas para el admin"""
    ventas = sistema.consultar_ventas()
    
    if not ventas:
        print("No hay ventas registradas.")
        return
    
    print("\n--- REPORTE DE VENTAS ---")
    print(f"{'Código':<8} {'Ruta':<25} {'Vendidas':<10} {'Ingresos':<12} {'Pasajeros'}")
    print("-" * 80)
    
    total_ingresos = 0
    total_sillas = 0
    total_pasajeros = 0
    
    for codigo, data in ventas.items():
        vuelo = data['vuelo']
        ruta = f"{vuelo.getOrigen()} → {vuelo.getDestino()}"
        sillas = data['sillas_vendidas']
        ingresos = data['ingresos']
        num_pasajeros = len(data['pasajeros'])
        
        print(f"{codigo:<8} {ruta:<25} {sillas:<10} ${ingresos:<11,} {num_pasajeros}")
        
        total_ingresos += ingresos
        total_sillas += sillas
        total_pasajeros += num_pasajeros
    
    print("-" * 80)
    print(f"TOTALES: {'':<25} {total_sillas:<10} ${total_ingresos:<11,} {total_pasajeros}")
    
    # Mostrar detalles de pasajeros si se solicita
    detalle = input("\n¿Mostrar detalles de pasajeros? (s/n): ").strip().lower()
    if detalle == 's':
        for codigo, data in ventas.items():
            print(f"\n--- PASAJEROS VUELO {codigo} ---")
            for i, pasajero in enumerate(data['pasajeros'], 1):
                print(f"{i}. {pasajero['nombre']} - {pasajero['id']}")

def ver_todos_vuelos_admin(sistema):
    """Muestra todos los vuelos para el admin"""
    if not sistema.vuelos:
        print("No hay vuelos registrados.")
        return
    
    print("\n--- TODOS LOS VUELOS ---")
    print(f"{'Código':<8} {'Origen':<12} {'Destino':<12} {'Horario':<10} {'Pref T/D':<10} {'Eco T/D':<10}")
    print("-" * 75)
    
    for vuelo in sistema.vuelos.values():
        pref_info = f"{vuelo.sillas_preferencial_total}/{vuelo.sillas_preferencial_disponibles}"
        eco_info = f"{vuelo.sillas_economica_total}/{vuelo.sillas_economica_disponibles}"
        
        print(f"{vuelo.getCodigo():<8} {vuelo.getOrigen():<12} {vuelo.getDestino():<12} "
              f"{vuelo.getHora():<10} {vuelo.getDia():<10} {pref_info:<10} {eco_info:<10}")

# Función principal del programa

def main():
    sistema = SistemaReservas()
    print("Bienvenido al Sistema de Reservas de Vuelos")
    
    while True:
        mostrar_menu_principal()
        
        try:
            opcion = int(input("Seleccione una opción: "))
            
            if opcion == 1:
                registrar_usuario(sistema)
            
            elif opcion == 2:
                if iniciar_sesion(sistema):
                    # Menú de usuario
                    while sistema.usuario_actual:
                        mostrar_menu_usuario()
                        
                        try:
                            opcion_usuario = int(input("Seleccione una opción: "))
                            
                            if opcion_usuario == 1:
                                buscar_vuelos(sistema)
                            elif opcion_usuario == 2:
                                realizar_reserva(sistema)
                            elif opcion_usuario == 3:
                                gestionar_reservas(sistema)
                            elif opcion_usuario == 4:
                                realizar_check_in(sistema)
                            elif opcion_usuario == 5:
                                cambiar_contraseña(sistema)
                            elif opcion_usuario == 6:
                                sistema.usuario_actual = None
                                print("Sesión cerrada.")
                            else:
                                print("✗ Opción inválida.")
                        
                        except ValueError:
                            print("✗ Entrada inválida.")
                        except KeyboardInterrupt:
                            print("\nSaliendo...")
                            sistema.usuario_actual = None
            
            elif opcion == 3:
                if acceso_admin(sistema):
                    # Menú de administrador
                    admin_activo = True
                    while admin_activo:
                        mostrar_menu_admin()
                        
                        try:
                            opcion_admin = int(input("Seleccione una opción: "))
                            
                            if opcion_admin == 1:
                                agregar_vuelo_admin(sistema)
                            elif opcion_admin == 2:
                                modificar_vuelo_admin(sistema)
                            elif opcion_admin == 3:
                                consultar_ventas_admin(sistema)
                            elif opcion_admin == 4:
                                ver_todos_vuelos_admin(sistema)
                            elif opcion_admin == 5:
                                admin_activo = False
                                print("Volviendo al menú principal.")
                            else:
                                print("✗ Opción inválida.")
                        
                        except ValueError:
                            print("✗ Entrada inválida.")
                        except KeyboardInterrupt:
                            print("\nVolviendo al menú principal...")
                            admin_activo = False
            
            elif opcion == 4:
                print("Gracias por usar el Sistema de Reservas de Vuelos!")
                break
            
            else:
                print("✗ Opción inválida.")
        
        except ValueError:
            print("✗ Entrada inválida.")
        except KeyboardInterrupt:
            print("\n\nSaliendo del sistema...")
            break
        
        # Pausa para que el usuario pueda leer los mensajes
        if opcion != 4:
            input("\nPresione Enter para continuar...")

if __name__ == '__main__':
    main()