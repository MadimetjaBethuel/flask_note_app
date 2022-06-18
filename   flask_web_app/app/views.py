from flask import Blueprint, render_template, request, redirect, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Renders the home page after login, show list of task

    Add new note to the database

    args: None
    returns: rendered template
    """

    if request.method == 'POST':
        note = request.form.get('note')

        #check len of note 
        if len(note) < 1:
            flash('Note is too short', category='error')
        
        else: 

            #add new note to the database

            new_note = Note( note_data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully', category='success')
    
    return render_template('home.html', user=current_user)



@views.route('/delete-note', methods=['POST'])

def delete_note():

    """
    Delete a note from the database

    args: None
    returns: rendered template
    """

    #get the note id from the request

    note = json.loads(request.data)

    noteId = note['noteId']
    note = Note.query.get(noteId)

    #delete the note from the database

    if note :
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully', category='success')
    
    return jsonify({})

