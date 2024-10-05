from flask import Flask #Se importa Flask.
from flask_sqlalchemy import SQLAlchemy #Flask para SQL  DBS
from os import path
from flask_login import LoginManager
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
    
    #Esto registra nuestros blueprints y le dice a python en que prefijo ir a buscar nuestras paginas.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager() # importas la funcion de login manager a login_manager
    login_manager.login_view = 'auth.login' #si no estoy login in a que ruta me manda
    login_manager.init_app(app)#En que aplicacion estamos trabajando

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app 

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():    
            db.create_all()
        print('Created Database!')

