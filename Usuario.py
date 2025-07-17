import hashlib

class Usuario:
    def __init__(self, nombre, id, email, contraseña=""):
        self.nombre = nombre
        self.id = id
        self.email = email
        self._hash = hashlib.sha256(contraseña.encode()).hexdigest() if contraseña else ""
        self.reservas = []
        self.millas = 0

    def getNombre(self):
        return self.nombre

    def getId(self):
        return self.id

    def getEmail(self):
        return self.email

    def getContraseña(self):
        return self._hash

    def setNombre(self, n):
        self.nombre = n

    def setId(self, i):
        self.id = i

    def setEmail(self, e):
        self.email = e

    def setContraseña(self, contraseña):
        self._hash = hashlib.sha256(contraseña.encode()).hexdigest()

    def verificarContraseña(self, contraseña):
        return self._hash == hashlib.sha256(contraseña.encode()).hexdigest()
