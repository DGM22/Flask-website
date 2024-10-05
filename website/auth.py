from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required,logout_user, current_user

auth = Blueprint('auth', __name__)


#Aqui se crearon tres diferentes paginsa creanto su rutas, dejando el url como 5000/login. de igual forma con las demas rutas
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully', category='success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect pasword, try again!')
        else:
            flash('Email dose not exist', category= 'error' )


    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'] )
def sign_up():
    #Se hace un http request a un form cuando es POST y se piden todos los inputs de tu forms  
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        # Se ponene limitantes para los inputs que estamos pidiendo liberando un mensaje de error o de succes si es que se hizo correctamente 
        if user:
            flash('Email all ready exists!', category='error')
        elif len(email) < 4:
            flash('Email most be grader than 4 caracters', category='error')
        elif len(first_name) < 3:
            flash('firstName most be grader than 3 caracters', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:
            flash('password most atleast 7 caracters', category='error')
        else:
            # Estamos creando al usuario y utilizando parametros de seguridad par crear un pasword hash el cual permite que al tener la base de datos no se pueda saber cuales son las contraseñas, en este caso usamos pbkdf2 es el algoritmo que si permite usar el metodo sha256 
            new_user = User(email = email, first_name= first_name, password = generate_password_hash(password1, method='pbkdf2:sha256') ) 
            db.session.add(new_user)
            db.session.commit() 
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)