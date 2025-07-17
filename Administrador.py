from Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, nombre, id, email, contraseña=""):
        super().__init__(nombre, id, email, contraseña)
