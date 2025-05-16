import pytest
from flask_login import login_user
from app.models import HealthRecord, User
from datetime import datetime

def login_test_user(client, test_user):
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302  # Redirect
    assert '/login' in response.headers['Location']

def test_dashboard_renders_without_data(client, test_user):
    login_test_user(client, test_user)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b"No data uploaded yet" in response.data

def test_dashboard_renders_with_data(client, test_user, app):
    with app.app_context():
        record = HealthRecord(
            user_id=test_user.id,
            date=datetime(2025, 5, 1),
            steps=8000,
            sleep_hours=7.5,
            mood=3
        )
        from app import db
        db.session.add(record)
        db.session.commit()

    login_test_user(client, test_user)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b"Sleep" in response.data  # One of the summary card labels
    assert b"Analysis Summary" in response.data
