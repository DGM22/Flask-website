from . import db # de todo el paquete se importa el objeto db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model): # Crea el objeto dde Notas que va a la base de datos
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Relaciona el id del usuari con una nota en espesifico



class User(db.Model,UserMixin): # Crear el usuario que va a la base de datos 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name  = db.Column(db.String(150))
    notes = db.relationship('Note') #Relaciona las Notas con el ususrario
