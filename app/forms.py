from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import Optional


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    height = StringField('Height (cm)', validators=[DataRequired()])
    weight = StringField('Weight (kg)', validators=[DataRequired()])
    medical_conditions = TextAreaField('Medical Conditions', validators=[Length(max=300)])

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField('About Me', validators=[Length(0, 200)])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[Optional()])

    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    height = FloatField('Height (cm)', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    medical_conditions = TextAreaField('Medical Conditions', validators=[Optional()])

    submit = SubmitField('Save Changes')
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Contact')
class PersonalizedMessageForm(FlaskForm):
     message = TextAreaField('Personalized Message (Optional)')