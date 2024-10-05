from flask import Blueprint, render_template, request, flash, jsonify  #Se importa blueprints 
from flask_login import  login_required, current_user
from .models import Note
from . import db
import json
#Se define nuestro blueprint el cual nos permitira crear diferentes rutas
views = Blueprint('views', __name__)

@views.route('/', methods= ['GET','POST'])#Ruta
@login_required
def home(): #La funcion de la ruta 
    if request.method == 'POST':
       note = request.form.get('note')
       
       if len(note) < 1:
        flash('Note is too short', category='error')
       else:
          new_note = Note(data=note, user_id=current_user.id)
          db.session.add(new_note)
          db.session.commit()
          flash('note addded!', category='success')


    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
