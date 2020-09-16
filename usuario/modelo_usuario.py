from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database import db
from martin_metodos import error

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(250))
    contrasena = db.Column(db.String(250))

class Usuario(UserMixin):

    def __init__(self, id_usuario, nombre_usuario, contrasena):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena

    def __repr__(self):
        return self.nombre_usuario

    def get_id(self):
        try:
            return str(self.id_usuario)
        except AttributeError:
            raise NotImplementedError('Sin el atributo id_usuario se anula get_id')

def validar_contrasena(nombre_usuario, contrasena):
    usuarios = Usuarios.query
    for usuario in usuarios:
        if usuario.nombre_usuario == nombre_usuario:
            return check_password_hash(usuario.contrasena, contrasena)
    return False

def obtener_usuario(nombre_usuario):
    nombre_usuario=str(nombre_usuario)
    usuarios = Usuarios.query
    if usuarios:
        for usuario in usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                return Usuario(
                    usuario.id_usuario,
                    usuario.nombre_usuario,
                    usuario.contrasena
                )
    return None