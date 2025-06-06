from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, SelectMultipleField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired


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
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
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
class ManualDataForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    steps = IntegerField('Steps', validators=[DataRequired()])
    sleep = FloatField('Sleep Hours', validators=[DataRequired()])
    mood = FloatField('Mood', validators=[DataRequired()])
    submit = SubmitField('Submit')
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Contact')
class ShareDataForm(FlaskForm):
    visualizations = SelectMultipleField('Visualizations', choices=[
        ('steps', 'Step Count'),
        ('sleep_hours', 'Sleep Patterns'),
        ('moods', 'Mood Distribution'),
        ('sleep_vs_mood', 'Sleep vs Mood'),
    ], validators=[DataRequired()])
    contacts = SelectMultipleField('Contacts', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Share Now')
class PersonalizedMessageForm(FlaskForm):
     message = TextAreaField('Personalized Message (Optional)')
class UploadForm(FlaskForm):
    file = FileField('Upload CSV', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload')

class LogoutForm(FlaskForm):
    pass
