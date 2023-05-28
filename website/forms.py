from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        Length(max=150, message='First name must be less than 150 characters.')
    ])
    last_name = StringField('Last Name', validators=[
        Length(max=150, message='Last name must be less than 150 characters.')
    ])
    about_me = TextAreaField('About Me', validators=[
        Length(max=1000, message='About me must be less than 1000 characters.')
    ])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[
        DataRequired(message='Please enter your date of birth.')
    ])
    favorite_animal = StringField('Favorite Animal', validators=[
        Length(max=100, message='Favorite animal must be less than 100 characters.'),
        Regexp(r'^[a-zA-Z ]*$', message='Favorite animal can only contain letters and spaces.')
    ])
    location = StringField('Location', validators=[
        Length(max=150, message='Location must be less than 150 characters.')
    ])
    interests = TextAreaField('Interests', validators=[
        Length(max=500, message='Interests must be less than 500 characters.')
    ])

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')