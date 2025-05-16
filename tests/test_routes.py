import io
import os
import pytest
from flask import url_for
from app.models import User
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db

# ✅ Test: Public home/index route
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"HealthWhisper" in response.data  # Check if branding is shown

# ✅ Test: Registration page loads
def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Get Started" in response.data  # Form CTA text

# ✅ Test: Login page loads
def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

# ✅ Test: Dashboard redirects if not logged in
def test_protected_dashboard_redirects(client):
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302  # Expected redirect
    assert '/login' in response.headers['Location']

# ✅ Test: Successful login flow for existing user
def test_successful_login(app, client):
    # Setup: create test user in DB
    user = User(
        name="Test User",
        email="test@example.com",
        gender="Male",
        dob=datetime(1990, 1, 1),
        height=175.0,
        weight=70.0,
        medical_conditions="None"
    )
    user.set_password("testpass")

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Action: login with correct credentials
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)

    # Assert: redirected to dashboard
    assert b"Login successful!" in response.data
    assert b"Dashboard" in response.data or response.status_code == 200

# ✅ Test: Logout after login
def test_logout_flow(app, client):
    # Setup: create and login test user
    user = User(
        name="Test User",
        email="test@example.com",
        gender="Male",
        dob=datetime(1990, 1, 1),
        height=175.0,
        weight=70.0,
        medical_conditions="None"
    )
    user.set_password("testpass")

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Login and then logout
    client.post('/login', data={'email': 'test@example.com', 'password': 'testpass'})
    response = client.post('/logout', follow_redirects=True)

    assert b"You have been logged out." in response.data
    assert b"Login" in response.data

# ✅ Test: Upload route handles valid CSV properly
def test_file_upload(client, app):
    # Setup: register and login uploader
    user = User(
        name="Uploader",
        email="upload@example.com",
        gender="Male",
        dob=datetime(1990, 1, 1),
        height=180,
        weight=80,
        medical_conditions="None"
    )
    user.set_password("uploadpass")

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={'email': 'upload@example.com', 'password': 'uploadpass'})

    # Upload valid CSV file
    with open(os.path.join("tests", "uploads", "sample_valid.csv"), "rb") as f:
        data = {'file': (f, 'sample_valid.csv')}
        response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200
    assert b"File uploaded and data saved successfully!" in response.data

# ✅ Test: Dashboard displays correctly with seeded data
def test_dashboard_with_seeded_data(authenticated_client, seed_health_data):
    response = authenticated_client.get('/dashboard')
    assert response.status_code == 200
    assert b"Trend Score" in response.data  # Summary card
    assert b"Analysis Summary" in response.data  # Analysis section

# ✅ Test: Login fails with wrong credentials
def test_login_failure_invalid_credentials(client):
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid credentials" in response.data

# ✅ Test: Registration fails with duplicate email
def test_register_existing_email(client, app):
    # Setup: manually create existing user
    user = User(
        name="Existing User",
        email="existing@example.com",
        gender="Male",
        dob=datetime(1990, 1, 1),
        height=175,
        weight=70,
        medical_conditions="None"
    )
    user.set_password("password123")

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Try to register again with the same email
    response = client.post('/register', data={
        'name': 'Someone',
        'email': 'existing@example.com',
        'password': 'newpass',
        'confirm_password': 'newpass',
        'gender': 'female',
        'dob': '1995-05-05',
        'height': 160,
        'weight': 55,
        'medical_conditions': '',
        'submit': 'Create Account'
    }, follow_redirects=True)
    
    print(response.data.decode())
    assert response.status_code == 200
    assert b"email address is already in use" in response.data.lower()

