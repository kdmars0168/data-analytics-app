import os
from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required,current_user
from app.utils import generate_analysis_summary
from app.forms import EditProfileForm 
from app.models import User, Contact 
from datetime import datetime
from app.forms import ContactForm

# Create a Blueprint called 'main'
main = Blueprint('main', __name__)

# Landing Page
@main.route('/')
def index():
    return render_template('index.html')

# Register Page
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address is already in use. Please choose a different one.', 'danger')
            return redirect(url_for('main.register'))

        # If email does not exist, create the new user
        user = User(name=form.name.data, email=form.email.data, gender=form.gender.data,
    dob=form.dob.data,
    height=form.height.data,
    weight=form.weight.data,
    medical_conditions=form.medical_conditions.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

# Login Page
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)

# Dashboard Page
@main.route('/dashboard')
@login_required
def dashboard():
    # Demo: In a real app, you would pull user-specific uploaded data
    user_data = {
        'steps': [117200, 8500, 9100, 7000, 10400, 11500, 9600],
        'sleep': [7, 6.5, 8, 7, 6, 8.5, 9],
        'mood': [8, 7, 9, 6, 8, 9, 10],
    }

    analysis = generate_analysis_summary(user_data)

    return render_template('dashboard.html', analysis=analysis)

# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

# Upload page
@main.route('/upload')
@login_required
def upload():
    return render_template('upload.html')  # (create upload.html later even if empty for now)

@main.route('/download_template')
@login_required
def download_template():
    # Define the directory where the template is located
    template_dir = os.path.join(current_app.root_path, 'static', 'assets')
    # Return the file as a download
    return send_from_directory(template_dir, 'template.csv', as_attachment=True)

@main.route('/submit_manual', methods=['POST'])
@login_required
def submit_manual():

    flash('Manual data submitted successfully!', 'success')
    return redirect(url_for('main.upload')) 

@main.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    form = ContactForm()

    if form.validate_on_submit():
        # Check if the contact already exists for this user
        existing_contact = Contact.query.filter_by(name=form.name.data, user_id=current_user.id).first()

        if existing_contact:
            flash('Contact name already exists.', 'danger')
        else:
            # Create and add the new contact
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                user_id=current_user.id 
            )
            db.session.add(contact)
            db.session.commit()
            flash('Contact added!', 'success')

        return redirect(url_for('main.share'))

   
    contacts = Contact.query.filter_by(user_id=current_user.id).all()

    return render_template('share.html', form=form, contacts=contacts)
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
@main.route('/profile/save', methods=['POST'])
@login_required
def save_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    gender = request.form.get('gender')
    dob_str = request.form.get('dob')
    height = request.form.get('height')
    weight = request.form.get('weight')
    medical_conditions = request.form.get('medical_conditions')

    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
    except ValueError:
        flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
        return redirect(url_for('main.profile'))


    current_user.name = name
    current_user.email = email
    current_user.gender = gender
    current_user.dob = dob
    current_user.height = float(height) if height else None
    current_user.weight = float(weight) if weight else None
    current_user.medical_conditions = medical_conditions

    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while saving your profile: ' + str(e), 'error')
        return redirect(url_for('main.profile'))