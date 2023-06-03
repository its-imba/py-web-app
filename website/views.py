"""
This module defines the views for the website.
"""
import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, UserProfile, Friendship, FriendshipRequest
from . import db
from .forms import ProfileForm, SearchForm

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

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Handle the edit profile functionality.
    """
    form = ProfileForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.user_profile.first_name = form.first_name.data
            current_user.user_profile.last_name = form.last_name.data
            current_user.user_profile.about_me = form.about_me.data
            current_user.user_profile.date_of_birth = form.date_of_birth.data
            current_user.user_profile.favorite_animal = form.favorite_animal.data
            current_user.user_profile.location = form.location.data
            current_user.user_profile.interests = form.interests.data
            db.session.commit()
            flash('Profile updated!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid input', category='error')

    # Pre-populate the form fields with the current user's data
    form.first_name.data = current_user.user_profile.first_name
    form.last_name.data = current_user.user_profile.last_name
    form.about_me.data = current_user.user_profile.about_me
    form.date_of_birth.data = current_user.user_profile.date_of_birth
    form.favorite_animal.data = current_user.user_profile.favorite_animal
    form.location.data = current_user.user_profile.location
    form.interests.data = current_user.user_profile.interests

    return render_template('edit-profile.html', user=current_user, form=form)

@views.route('/search', methods=['GET', 'POST'])
@login_required  # Assuming you are using a login_required decorator
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        results = User.query.filter(UserProfile.first_name.ilike(f'%{query}%')).all()
        return render_template('search_results.html', results=results, user=current_user)
    return render_template('search.html', form=form, user=current_user)


@views.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        # Handle the case when the user does not exist
        flash('User not found.', 'danger')
        return redirect(url_for('views.home'))

    user_profile = user.user_profile
    friends = user.friends.all() if user.friends else None
    received_friend_requests = FriendshipRequest.query.filter_by(receiver_id=user_id, status='pending').all()

    return render_template('profile.html', user=user_profile, friends=friends, received_friend_requests=received_friend_requests)




@views.route('/add_friend/<int:user_id>', methods=['POST'])
@login_required
def add_friend(user_id):
    """
    Sends a friend request to another user.
    """
    try:
        friend = User.query.get(user_id)

        if friend:
            # Check if a friend request has already been sent
            if current_user.sent_friend_requests.filter_by(receiver_id=user_id).first():
                flash('Friend request already sent', category='error')
            # Check if the user is already friends with the friend
            elif current_user.friends.filter_by(id=user_id).first():
                flash('You are already friends with this user', category='error')
            else:
                # Create a new friendship request
                friendship_request = FriendshipRequest(sender_id=current_user.id, receiver_id=user_id)
                db.session.add(friendship_request)
                db.session.commit()
                flash('Friend request sent', category='success')
        else:
            flash('User not found', category='error')
    except Exception as error:
        flash('An error occurred while sending the friend request', category='error')
        print(str(error))

    return redirect(url_for('views.profile', user_id=user_id))


@views.route('/accept_friend/<int:request_id>', methods=['POST'])
@login_required
def accept_friend(request_id):
    """
    Accepts a friend request from another user.
    """
    try:
        request = FriendshipRequest.query.get(request_id)

        if request:
            friendship = Friendship(user_id=request.sender_id, friend_id=current_user.id, status='accepted')
            db.session.add(friendship)
            db.session.delete(request)
            db.session.commit()
            flash('Friend request accepted', category='success')
        else:
            flash('Friend request not found', category='error')
    except Exception as error:
        flash('An error occurred while accepting the friend request', category='error')
        print(str(error))

    # Update the friend request status for the other user involved in the friendship
    FriendshipRequest.query.filter_by(sender_id=current_user.id, receiver_id=request.sender_id).update({"status": "accepted"})
    db.session.commit()

    return redirect(url_for('views.profile', user_id=current_user.id))




@views.route('/reject_friend/<int:user_id>', methods=['POST'])
@login_required
def reject_friend(user_id):
    """
    Rejects a friend request from another user.
    """
    try:
        friend = User.query.get(user_id)

        if friend:
            friendship = Friendship.query.filter_by(user_id=user_id, friend_id=current_user.id).first()
            if friendship:
                db.session.delete(friendship)
                db.session.commit()
                flash('Friend request rejected', category='success')
            else:
                flash('Friend request not found', category='error')
        else:
            flash('User not found', category='error')
    except Exception as error:
        flash('An error occurred while rejecting the friend request', category='error')
        print(str(error))

    return redirect(url_for('views.profile', user_id=current_user.id))

