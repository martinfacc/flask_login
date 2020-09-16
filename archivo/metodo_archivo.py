from flask_name import app
from database import db
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from datetime import datetime, date
from archivo.modelo_archivo import Archivos
from usuario.modelo_usuario import obtener_usuario
from usuario.metodo_login import login

app.config['UPLOAD_FOLDER']='./static/archivos'

@app.route("/archivo/subir", methods=['GET', 'POST'])
def subir():
    if not current_user.is_authenticated: return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            f = request.files['archivo']
            nombre_del_archivo = secure_filename(f.filename)
            tupla=os.path.splitext(nombre_del_archivo)
            if tupla[1]=='.pdf':
                archivo = Archivos(
                    nombre='',
                    carpeta=app.config['UPLOAD_FOLDER'],
                    descripcion=request.form.get('descripcion'),
                    fechahora=datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
                    id_usuario=obtener_usuario(current_user).id_usuario,
                    estado=1
                )
                db.session.add(archivo)
                db.session.flush()
                archivo.nombre = str(archivo.id)+'_'+str(date.today())
                f.save(os.path.join(archivo.carpeta, archivo.nombre))
                db.session.commit()
                return render_template(
                    '/archivo/subir.html',
                    alert_success=True,
                    nombre=archivo.nombre
                )
            else: 
                return render_template(
                    '/archivo/subir.html',
                    alert_error=True,
                    mensaje_error='Error, solo se permiten archivos pdf'
                )
        except Exception as e:
            return render_template(
                '/archivo/subir.html',
                alert_error=True,
                mensaje_error=f'Error: {e}'
            )
    return render_template('/archivo/subir.html')