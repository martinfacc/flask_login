from database import db

class Archivos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    carpeta = db.Column(db.String(50))
    descripcion= db.Column(db.String(150))
    fechahora = db.Column(db.DateTime)
    id_usuario = db.Column(db.Integer)
    estado = db.Column(db.Integer)