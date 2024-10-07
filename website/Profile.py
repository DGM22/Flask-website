from flask import Blueprint, render_template, request
from flask_login import current_user
from .models import User

profile = Blueprint('profile', __name__)

@profile.route('/profile')
def Profile():

    return render_template('profile.html', user = current_user )
