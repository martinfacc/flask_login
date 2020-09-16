from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_name import app
from database import db
from flask_migrate import Migrate
from usuario.modelo_usuario import Usuarios, Usuario
import usuario.metodo_login
from persona.metodo_abm import personal
from archivo.metodo_archivo import subir


#Configuración de la bd
FULL_URL_DB = 'postgresql://postgres:pythonboys@104.128.65.42:5050/Organismo'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

app.config['SECRET_KEY']='llave_secreta'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id_usuario):
    usuarios = Usuarios.query
    for usuario in usuarios:
        if usuario.id_usuario == int(id_usuario):
            return Usuario(usuario.id_usuario,usuario.nombre_usuario,usuario.contrasena)
    return None

@app.route("/")
def inicio():
    return redirect(url_for('personal'))

