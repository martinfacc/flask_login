from database import db
from martin_metodos import error
from flask import request

def dict_to_model(data, model): 
    for key, value in data.items():
        if hasattr(model, key): 
            setattr(model, key, value)  

class Persona(db.Model):
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    cuil = db.Column(db.BigInteger)
    documento = db.Column(db.Integer)
    correo_ofi = db.Column(db.String(100))
    correo_priv = db.Column(db.String(100))
    dependencia = db.Column(db.String(100))
    subsecretaria = db.Column(db.String(100))
    secretaria = db.Column(db.String(100))
    baja = db.Column(db.Boolean, nullable=False)
    contrato = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    base_rrhh = db.Column(db.Boolean)
    celular = db.Column(db.String(50))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_persona': self.id_persona,
            'nombre': self.nombre,
            'apellido':  self.apellido,
            'cuil' : self.cuil,
            'documento' : self.documento,
            'correo_ofi' : self.correo_ofi,
            'correo_priv' : self.correo_priv,
            'dependencia' : self.dependencia,
            'subsecretaria' : self.subsecretaria,
            'secretaria' : self.secretaria,
            'baja' : self.baja,
            'contrato' : self.contrato,
            'cargo' : self.cargo,
            'base_rrhh' : self.base_rrhh,
            'celular' : self.celular

            # 'modified_at': dump_datetime(self.modified_at),
            # This is an example how to deal with Many2Many relations
            # 'many2many'  : self.serialize_many2many
        }

    # @property
    # def serialize_many2many(self):
        """
        Return object's relations in easily serializable format.
        NB! Calls many2many's serialize property.
        """
    #   return [ item.serialize for item in self.many2many]

def obtener_datos_form():
    diccionario={}; lista=[]
    def comprobar(texto):
        if texto == 'True': return True
        return False

    tupla_exclusion = ('id_persona', 'serialize', '_sa_class_manager', 'baja', 'base_rrhh')
    for i in tupla_exclusion[3:]: diccionario[i]=comprobar(request.form.get(i))
    dic_aux = {k:v for k, v in Persona.__dict__.items() if k not in tupla_exclusion}
    for key, value in dic_aux.items(): lista.append(key)
    for i in lista: diccionario[i]=request.form.get(i)
    return diccionario
