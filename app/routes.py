import os
from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required,current_user
from app.utils import generate_analysis_summary
from app.forms import EditProfileForm
from app.models import User 


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
        user = User(name=form.name.data, email=form.email.data)
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

# Share page
@main.route('/share')
@login_required
def share():
    return render_template('share.html')  # (create share.html later even if empty for now)
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('edit_profile.html', form=form)
