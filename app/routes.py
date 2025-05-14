import os, json
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, send_from_directory, current_app
from app import db
from app.forms import RegistrationForm, LoginForm, EditProfileForm
from app.models import User, UploadedData, SharedData, HealthRecord
from flask_login import login_user, logout_user, login_required, current_user
from app.utils import generate_analysis_summary
from sqlalchemy import extract
import csv
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import defaultdict
from statistics import mean
from app.forms import EditProfileForm, ContactForm
from app.models import User, Contact

# Create a Blueprint called 'main'
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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

@main.route('/dashboard')
@login_required
def dashboard():
    records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(HealthRecord.date).all()

    if not records:
        chart_data = {
            "daily": {"labels": [], "steps": [], "sleep": [], "mood": []},
            "weekly": {"labels": [], "steps": [], "sleep": [], "mood": []},
            "monthly": {"labels": [], "steps": [], "sleep": [], "mood": []},
            "yearly": {"labels": [], "steps": [], "sleep": [], "mood": []}
        }
        analysis = {
            "steps_analysis": "No data uploaded yet.",
            "sleep_patterns": "No data uploaded yet.",
            "mood_correlation": "No data uploaded yet.",
            "recommendations": "Upload data to see insights."
        }
        summary = {
            "average_steps": 0,
            "sleep_quality": 0,
            "average_mood": 0,
            "trend_score": 0
        }
    else:
        grouped = {
            "daily": defaultdict(list),
            "weekly": defaultdict(list),
            "monthly": defaultdict(list),
            "yearly": defaultdict(list)
        }

        for r in records:
            grouped["daily"][r.date].append(r)
            grouped["weekly"][r.date.isocalendar()[1]].append(r)
            grouped["monthly"][(r.date.year, r.date.month)].append(r)
            grouped["yearly"][r.date.year].append(r)

        def reduce(group_dict, label_format, limit=None):
            items = list(group_dict.items())
            items.sort(key=lambda x: x[0])
            if limit:
                items = items[-limit:]
            return {
                "labels": [label_format(k) for k, _ in items],
                "steps": [int(mean([r.steps for r in v])) for _, v in items],
                "sleep": [float(mean([r.sleep_hours for r in v])) for _, v in items],
                "mood": [float(mean([r.mood for r in v])) for _, v in items],
            }

        chart_data = {
            "daily": reduce(grouped["daily"], lambda d: d.strftime("%Y-%m-%d"), limit=7),
            "weekly": reduce(grouped["weekly"], lambda w: f"Week {w}", limit=6),
            "monthly": reduce(grouped["monthly"], lambda ym: f"{ym[0]}-{ym[1]:02d}", limit=6),
            "yearly": reduce(grouped["yearly"], lambda y: str(y))
        }

        analysis = generate_analysis_summary(chart_data["daily"])
        summary = {
            "average_steps": int(mean([r.steps for r in records])),
            "sleep_quality": round(mean([r.sleep_hours for r in records]), 1),
            "average_mood": round(mean([r.mood for r in records]), 1),
            "trend_score": 87  # Placeholder for real trend logic
        }

    return render_template(
        "dashboard.html",
        chart_data=json.dumps(chart_data),
        analysis=analysis,
        summary=summary
    )

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)

            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    try:
                        record = HealthRecord(
                            user_id=current_user.id,
                            date=datetime.strptime(row['date'].strip(), "%Y-%m-%d").date(),
                            steps=int(row['steps'].strip()),
                            sleep_hours=float(row['sleep_hours'].strip()),
                            mood=int(row['mood'].strip()),
                        )
                        db.session.add(record)
                        count += 1
                    except Exception as e:
                        print(f"Skipping row due to error: {e}")
                db.session.commit()
                print(f"[DEBUG] Uploaded {count} records for user ID {current_user.id}")

            flash('File uploaded and data saved successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid file format. Please upload a CSV file.', 'danger')

    return render_template('upload.html')

@main.route('/download_template')
@login_required
def download_template():
    template_dir = os.path.join(current_app.root_path, 'static', 'assets')
    return send_from_directory(template_dir, 'template.csv', as_attachment=True)

@main.route('/submit_manual', methods=['POST'])
@login_required
def submit_manual():
    date = request.form['date']
    steps = request.form['steps']
    sleep = request.form['sleep']
    mood = request.form['mood']

    record = HealthRecord(
        user_id=current_user.id,
        date=datetime.strptime(date, '%Y-%m-%d').date(),
        steps=int(steps),
        sleep_hours=float(sleep),
        mood=int(mood)
    )
    db.session.add(record)
    db.session.commit()
    flash('Manual data submitted successfully!', 'success')
    return redirect(url_for('main.upload'))


@main.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    form = ContactForm()

    if form.validate_on_submit():
        existing_contact = Contact.query.filter_by(name=form.name.data, user_id=current_user.id).first()
        if existing_contact:
            flash('Contact name already exists.', 'danger')
        else:
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


@main.route('/edit_profile', methods=['GET', 'POST'])

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