"""
This module defines the views for the website.
"""
import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Handles the home page functionality.
    """
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            try:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added', category='success')
            except Exception as error:
                flash('An error occurred while adding the note', category='error')
                print(str(error))

    try:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, notes=notes)
    except Exception as error:
        flash('An error occurred while fetching notes', category='error')
        print(str(error))

    return redirect(url_for('views.home'))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    """
    Deletes a note from the database.
    """
    try:
        note = json.loads(request.data)
        note_id = note['noteId']
        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    except Exception as error:
        flash('An error occurred while deleting the note', category='error')
        print(str(error))

    return jsonify({})

@views.route('/update-note', methods=['POST'])
@login_required
def update_note():
    """
    Updates a note in the database.
    """
    try:
        data = request.get_json()
        note_id = data['noteId']
        updated_note = data['updatedText']
        note = Note.query.get(note_id)

        if note and note.user_id == current_user.id:
            if len(updated_note) < 1:
                flash('Note is too short', category='error')
            else:
                note.data = updated_note
                db.session.commit()
                flash('Note updated', category='success')
                return jsonify(message='Note updated')
        else:
            flash('Note not found or you do not have permission to edit it', category='error')
    except Exception as error:
        flash('An error occurred while updating the note', category='error')
        print(str(error))

    return jsonify(message='Error')

@views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """
    Edits a note in the database.
    """
    try:
        note = Note.query.get(note_id)

        if note and note.user_id == current_user.id:
            if request.method == 'POST':
                new_note = request.json.get('updatedNote')

                if len(new_note) < 1:
                    flash('Note is too short', category='error')
                else:
                    note.data = new_note
                    db.session.commit()
                    flash('Note updated', category='success')
                    return jsonify(message='Note updated')

            return render_template('edit_note.html', user=current_user, note=note)
        else:
            flash('Note not found or you do not have permission to edit it', category='error')
    except Exception as error:
        flash('An error occurred while editing the note', category='error')
        print(str(error))

    return redirect(url_for('views.home'))
