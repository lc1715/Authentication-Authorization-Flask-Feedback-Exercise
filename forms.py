from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20, message='Maximum length of username is 20 characters. Please try again.')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])
    email = EmailField('Email', validators=[InputRequired(), Length(max=50), Email()])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30, message='Name cannot be longer than 30 chars') ])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30, message='Name cannot be longer than 30 chars')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),  Length(max=20, message='Maximum length of username is 20 characters. Please try again.')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = StringField('Content', validators=[InputRequired()])
    