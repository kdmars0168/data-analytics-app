from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    # your existing columns here
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    uploaded_data = db.relationship('UploadedData', backref='owner', lazy=True)
    shared_data = db.relationship('SharedData', backref='shared_with', lazy=True)
    gender = db.Column(db.String(10))  
    dob = db.Column(db.Date)           
    height = db.Column(db.Float)      
    weight = db.Column(db.Float)       
    medical_conditions = db.Column(db.Text)
    contacts = db.relationship('Contact', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UploadedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    file_path = db.Column(db.String(512), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    shared_data = db.relationship('SharedData', backref='data', lazy=True)

    def __repr__(self):
        return f'<UploadedData {self.filename}>'

class SharedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(db.Integer, db.ForeignKey('uploaded_data.id'))
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')

    def __repr__(self):
        return f'<SharedData {self.data_id} to {self.shared_with_user_id}>'

def load_user(user_id):
    return User.query.get(int(user_id))


class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    mood = db.Column(db.Integer, nullable=False)  # Mood score 1–10

    user = db.relationship('User', backref='health_records')


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    chart_type = db.Column(db.String(32))
