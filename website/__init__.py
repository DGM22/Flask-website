from flask import Flask, jsonify #Se importa Flask.
from flask_sqlalchemy import SQLAlchemy #Flask para SQL  DBS
from os import path
from flask_login import LoginManager
import json

#Se declara el objeto de la base de datos 
db = SQLAlchemy()
DB_NAME = "database.db"


#Se crea una funcion para asi crear el objeto app y configurarlo con una llave de acceso.
def create_app():
    app = Flask(__name__) # Esto le dice a flask donde esta el doc.
    app.config['SECRET_KEY'] = 'oasijdfaldkjf kldjflaksdj'
    #Decir al codigo donde se encuentra tu base de datos, utilizando path.join que creaa la ruta website/database.db y luego path.abspath que crea ya la tura comopleta por ejemplo C:\ruta\completa\hacia\proyecto\website\database.db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.abspath(path.join("website", DB_NAME))}' 


    #Inicialisar la base de datos
    db.init_app(app)

    #Importamos los blueprints
    from .view import views
    from .auth import auth
    from .Profile import profile
    
    #Esto registra nuestros blueprints y le dice a python en que prefijo ir a buscar nuestras paginas.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')

    from .models import User, Note, Acquisition

    create_database(app)

    login_manager = LoginManager() # importas la funcion de login manager a login_manager
    login_manager.login_view = 'auth.login' #si no estoy login in a que ruta me manda
    login_manager.init_app(app)#En que aplicacion estamos trabajando

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.route('/populate')
    def populate():
        # Datos de ejemplo que queremos insertar
        data = [
            {'year': 2010, 'count': 10},
            {'year': 2011, 'count': 20},
            {'year': 2012, 'count': 15},
            {'year': 2021, 'count': 50},
        ]

        # Iterar sobre los datos y agregar cada registro a la base de datos
        for item in data:
            acquisition = Acquisition(year=item['year'], count=item['count'])
            db.session.add(acquisition)
        
        # Confirmar los cambios en la base de datos
        db.session.commit()

        return "Base de datos poblada con éxito"
    
    @app.route('/api/acquisitions', methods=['GET'])
    def get_acquisitions():
        acquisitions = Acquisition.query.all()  # Obtener todos los registros de la base de datos
        # Convertir los registros en una lista de diccionarios (uno por cada adquisición)
        data = [{'year': acquisition.year, 'count': acquisition.count} for acquisition in acquisitions]
        return jsonify(data)  # Devolver los datos en formato JSON


    return app 

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():    
            db.create_all()
            print('Created Database!')
       

