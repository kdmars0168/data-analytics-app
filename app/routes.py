import os, json
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, send_from_directory, current_app
from app import db
from app.forms import RegistrationForm, LoginForm, EditProfileForm
from app.models import User, SharedData, HealthRecord
from flask_login import login_user, logout_user, login_required, current_user
from app.utils import generate_analysis_summary
from sqlalchemy import extract
import csv
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import defaultdict
from statistics import mean
from app.forms import EditProfileForm, ContactForm
from app.models import User, Contact, SharedData
from app.models import  PersonalizedMessage
from app.forms import PersonalizedMessageForm
from app.forms import ManualDataForm,ShareDataForm
from app.forms import UploadForm
from flask import request, flash, redirect, url_for, render_template

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
    form = UploadForm()

    if form.validate_on_submit():
        file = form.file.data
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

    return render_template('upload.html', form=form)


@main.route('/download_template')
@login_required
def download_template():
    template_dir = os.path.join(current_app.root_path, 'static', 'assets')
    return send_from_directory(template_dir, 'template.csv', as_attachment=True)

@main.route('/submit_manual', methods=['POST'])
@login_required
def submit_manual():
    form = ManualDataForm()
    if form.validate_on_submit():
        record = HealthRecord(
            user_id=current_user.id,
            date=form.date.data,
            steps=form.steps.data,
            sleep_hours=form.sleep.data,
            mood=form.mood.data
        )
        db.session.add(record)
        db.session.commit()
        flash('Manual data submitted successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('upload.html', form=form)
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Use 'name' instead of 'username'
        name = form.name.data
        gender = form.gender.data
        dob = form.dob.data
        height = form.height.data
        weight = form.weight.data
        medical_conditions = form.medical_conditions.data

        current_user.name = name
        current_user.gender = gender
        current_user.dob = dob
        current_user.height = height
        current_user.weight = weight
        current_user.medical_conditions = medical_conditions

        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while saving your profile: {e}', 'error')
            return redirect(url_for('main.profile'))

    if form.is_submitted():
        form.name.data = current_user.name
        form.gender.data = current_user.gender
        form.dob.data = current_user.dob
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        form.medical_conditions.data = current_user.medical_conditions

    return render_template('profile.html', form=form, user=current_user)


@main.route('/save_message', methods=['POST'])
@login_required
def save_message():
    data = request.get_json() 
    message_text = data.get('message')  
    if message_text is not None:
        existing_msg = PersonalizedMessage.query.filter_by(user_id=current_user.id).first()
        if existing_msg:
            existing_msg.message = message_text 
        else:
            new_msg = PersonalizedMessage(user_id=current_user.id, message=message_text)  
            db.session.add(new_msg)
        db.session.commit()
    return jsonify({'status': 'saved'}) 
@main.route('/share', methods=['GET'])
@login_required
def share():

    contact_form = ContactForm()
    share_form = ShareDataForm()


    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    share_form.contacts.choices = [(c.id, f"{c.name} - {c.email}") for c in contacts]

    message_text = ""

    return render_template('share.html',
                           share_form=share_form,
                           contact_form=contact_form,
                           contacts=contacts,
                           message_text=message_text)


@main.route('/add_contact', methods=['POST'])
@login_required
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data


        existing = Contact.query.filter_by(user_id=current_user.id, email=email).first()
        if existing:
            flash("This contact already exists.", "warning")
        else:
            new_contact = Contact(user_id=current_user.id, name=name, email=email)
            db.session.add(new_contact)
            db.session.commit()
            flash("Contact added successfully.", "success")
    else:
        flash("Invalid contact information.", "danger")

    return redirect(url_for('main.share'))


@main.route('/share_data', methods=['POST'])
@login_required
def share_data():
    selected_visuals = request.form.getlist('visualizations')
    selected_contacts = request.form.getlist('contacts')
    message_text = request.form.get('personalized_message', '')

    if not selected_visuals or not selected_contacts:
        flash("Please select at least one visualization and one contact.", "danger")
        return redirect(url_for('main.share'))

    for contact_id in selected_contacts:
        for vis in selected_visuals:
            shared = SharedData(
                shared_by_user_id=current_user.id,
                data_type=vis,
                shared_with_contact_email=Contact.query.get(contact_id).email
            )
            db.session.add(shared)
    db.session.commit()
    flash("Data shared successfully!", "success")
    return redirect(url_for('main.share'))


@main.route('/shared_with_me')
@login_required
def shared_with_me():
    shared_records = SharedData.query.filter_by(shared_with_contact_email=current_user.email).all()
    shared_by_user_ids = list(set(record.shared_by_user_id for record in shared_records))
    shared_users = User.query.filter(User.id.in_(shared_by_user_ids)).all()

    user_id = request.args.get('user_id', type=int)

    selected_user = None
    steps_data = []
    sleep_data = []
    mood_data = []
    sleep_vs_mood_data = []

    if user_id:
        selected_user = User.query.get(user_id)
        if selected_user:
            # 从 HealthRecord 表中获取该用户所有健康数据，按日期排序
            records = HealthRecord.query.filter_by(user_id=user_id).order_by(HealthRecord.date).all()

            # 组装数据格式：每条都是 {'date': 'YYYY-MM-DD', 'value': xxx}
            steps_data = [{'date': r.date.strftime('%Y-%m-%d'), 'steps': r.steps} for r in records]
            sleep_data = [{'date': r.date.strftime('%Y-%m-%d'), 'sleep_hours': r.sleep_hours} for r in records]
            mood_data = [{'date': r.date.strftime('%Y-%m-%d'), 'mood': r.mood} for r in records]

            # sleep_vs_mood_data 为二维数据，可以直接用 date, sleep_hours, mood
            sleep_vs_mood_data = [{'date': r.date.strftime('%Y-%m-%d'), 'sleep_hours': r.sleep_hours, 'mood': r.mood} for r in records]

    return render_template(
        'shared_with_me.html',
        shared_users=shared_users,
        selected_user=selected_user,
        steps_data=steps_data,
        sleep_data=sleep_data,
        mood_data=mood_data,
        sleep_vs_mood_data=sleep_vs_mood_data
    )
