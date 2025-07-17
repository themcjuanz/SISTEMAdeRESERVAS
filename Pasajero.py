from Usuario import Usuario

class Pasajero(Usuario):
    def __init__(self, nombre="", id=0, email="", contraseña=""):
        super().__init__(nombre=nombre, id=id, email=email)
        self.contraseña = contraseña
        self.silla = None