from flask_name import app
from database import db
from flask import Flask, render_template,request, url_for, redirect,Response,jsonify,json
from persona.modelo_persona import Persona, obtener_datos_form, dict_to_model
from flask_login import login_required
from martin_metodos import error
from sqlalchemy.exc import InvalidRequestError, DataError

@app.route('/personal')
def personal():
    personas = Persona.query
    return render_template('persona/personal_json.html',
                            personas=personas,
                            titulo='Listado del personal',
                            personalpage=True,
                            listado=True)

@app.route('/personaljson',methods=['GET', 'POST'])
def personaljson():
    personas = Persona.query
    objeto_return = {  
        'meta': {
        'page': 1,
        'pages': 1,
        'perpage': -1,
        'total': 350,
        'sort': 'asc',
        'field': 'RecordID'
    },
    'data': [ i.serialize for i in personas ]
        
    }
    return Response(json.dumps(objeto_return), mimetype='application/json')
    #return jsonify(objeto_return) 

@app.route('/altapersona',methods=['GET','POST'])
@login_required
def alta_persona():
    if request.method == 'POST':
        diccionario=obtener_datos_form()
        try:
            persona = Persona()
            dict_to_model(diccionario, persona)
            db.session.add(persona)
            db.session.flush()
            db.session.commit()        
            return jsonify(persona.serialize)
        except (InvalidRequestError, DataError, Exception) as e:
            db.session.rollback()
            return jsonify({ "error":e })
            
    return render_template('persona/editar_persona.html',
                            persona={},
                            titulo='Alta de persona',
                            editar = False,
                            listado=True )                  

@app.route('/eliminarpersona/<id>')
@login_required
def eliminar_persona(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('personal'))  

@app.route('/editarpersona/<id>', methods=['GET','POST'])
def editar_persona(id):
    alert_success = False; alert_error = False
    persona = Persona.query.get_or_404(id)
    if request.method == 'POST':
        diccionario=obtener_datos_form()
        try:
            dict_to_model(diccionario, persona)
            db.session.commit()
            return jsonify(persona.serialize)
           
        #te la dedico a vos Diego
        except (InvalidRequestError, DataError, Exception) as e:
            return jsonify({ "error":e })
            db.session.rollback()
            
    return render_template('persona/editar_persona.html',
                            titulo='Editar persona',
                            persona=persona,
                            id = id,
                            listado=True )

