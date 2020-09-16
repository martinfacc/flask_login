from flask_name import app
from database import db
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from usuario.modelo_usuario import Usuario, Usuarios, obtener_usuario, validar_contrasena

from martin_metodos import error

@app.route('/login', methods=['GET', 'POST'])
def login():
    recuerdame=False; alert_error=False; mensaje_error=''
    #Si el usuario ya esta logeado lo enviamos al inicio
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    if request.method=='POST':
        try:
            #Comprobamos el estado del checkbox 
            check = request.form.get('recuerdame')
            if check is not None:
                recuerdame = True
            #Obtenemos los datos ingresados en el form
            nombre_usuario=request.form.get('nombre_usuario')
            contrasena=request.form.get('contrasena')

            #Comprobamos si el usuario se encuentra en la base de datos
            # y creamos un objeto de la clase Usuario
            usuario = obtener_usuario(nombre_usuario)
            #Comprobamos que el usuario y la contraseña sean validos
            if bool(usuario) and validar_contrasena(nombre_usuario, contrasena):
                #Intentamos iniciar sesion con el usuario ingresado
                login_user(usuario, remember=recuerdame)

                #Si logramos iniciar sesion 
                if login_user:
                    return redirect(url_for('inicio'))
            else:
                alert_error = True
                mensaje_error='El usuario o la contraseña son invalidos'
        except Exception as e:
            alert_error = True;mensaje_error=e

    return render_template('usuario/login.html',
                        titulo='Iniciar sesión',
                        alert_error = alert_error,
                        mensaje_error=mensaje_error)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    alert_success=False; alert_error=False; mensaje_error=''

    #Si el usuario ya esta logeado lo enviamos al inicio
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        #Obtenemos los valores ingresados en el form
        nombre_usuario = request.form.get('nombre_usuario') 
        contrasena = request.form.get('contrasena') 
        contrasena_confirmar = request.form.get('contrasena_confirmar') 
        
        #Si el nombre de usuario ingresado no se encuentra en la bd
        if obtener_usuario(nombre_usuario) is None:

            #Si las contraseñas ingresadas coinciden
            if contrasena == contrasena_confirmar:

                #Creamos el usuario y lo guardamos
                usuario = Usuarios()
                usuario.nombre_usuario=nombre_usuario
                usuario.contrasena=generate_password_hash(contrasena)
                db.session.add(usuario)
                db.session.commit()
                
                login_user(obtener_usuario(nombre_usuario))

                #Si logramos logear entonces informamos al usuario
                if login_user:
                    alert_success=True
                else:
                    alert_error=True; mensaje_error='Ocurrio un error. Por favor vuelva a intentar nuevamente'
            
            #En caso de que las contraseñas sean iguales o que el
            #usuario ya este registrado
            else:
                alert_error=True; mensaje_error='Las contraseñas no coinciden'
        else:
            alert_error=True; mensaje_error=f'El usuario "{nombre_usuario}" ya existe'
    
    return render_template('usuario/signin.html',
                            titulo='Registrar nuevo usuario',
                            alert_success=alert_success,
                            alert_error=alert_error,
                            mensaje_error=mensaje_error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('inicio'))

@app.route('/editar_usuario', methods=['GET', 'POST'])
@login_required
def editar_usuario():
    usuario_actual = str(current_user)
    usuario = Usuarios.query.get(obtener_usuario(usuario_actual).id_usuario)
    alert_success = False;alert_error = False;mensaje_error=''

    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario') 
        contrasena = request.form.get('contrasena')
        nueva_contrasena = request.form.get('nueva_contrasena')
        c_nueva_contrasena = request.form.get('c_nueva_contrasena')

        if validar_contrasena(usuario_actual, contrasena):
            e_nombre_usuario = usuario_actual;e_contrasena = contrasena
            if not bool(nueva_contrasena):
                if nueva_contrasena==c_nueva_contrasena:
                    e_contrasena=nueva_contrasena
                else: 
                    alert_error=True;mensaje_error= f'Las contraseñas no coinciden' 
            
            if obtener_usuario(nombre_usuario) is None or nombre_usuario==usuario_actual:
                e_nombre_usuario = nombre_usuario
            else:
                alert_error=True; mensaje_error= f'El nombre de usuario "{nombre_usuario}" no está disponible' 

            if not nueva_contrasena==contrasena or not nombre_usuario==usuario_actual: 
                try:
                    usuario.nombre_usuario=e_nombre_usuario
                    usuario.contrasena=generate_password_hash(e_contrasena)
                    db.session.commit()
                    alert_success = True
                    login_user(obtener_usuario(e_nombre_usuario))
                except:
                    alert_error=True;mensaje_error='Ocurrio un error. Por favor vuelva a intentar nuevamente'

        else:
            alert_error=True; mensaje_error='Error de autentificación: la contraseña no es valida'
            

    return render_template('usuario/editar_usuario.html',
                            usuario = usuario,
                            titulo='Editar usuario',
                            alert_success = alert_success,
                            alert_error = alert_error,
                            mensaje_error=mensaje_error)       
