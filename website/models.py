"""
This module defines the models for the website.
"""
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Note(db.Model):
    """
    Represents a note in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    """
    Represents a user in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    user_profile = db.relationship('UserProfile', back_populates='user', uselist=False)

class UserProfile(db.Model):
    """
    Represents a user profile in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    about_me = db.Column(db.String(1000), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    favorite_animal = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    interests = db.Column(db.String(500), nullable=True)

    user = db.relationship('User', back_populates='user_profile')

