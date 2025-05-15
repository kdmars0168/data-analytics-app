import pytest
from app import create_app, db
from app.models import User, HealthRecord
from werkzeug.security import generate_password_hash
from datetime import date, timedelta

# Main test app fixture
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
        "UPLOAD_FOLDER": "tests"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# Flask test client
@pytest.fixture
def client(app):
    return app.test_client()

# Create test user (used in login + dashboard)
@pytest.fixture
def test_user(app):
    user = User(
        name="Test User",
        email="test@example.com",
        gender="Male",
        dob=date(1990, 1, 1),
        height=175.0,
        weight=70.0,
        medical_conditions="None"
    )
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()
    return user

# Authenticated client for protected route tests
@pytest.fixture
def authenticated_client(client, test_user):
    client.post("/login", data={
        "email": test_user.email,
        "password": "testpass"
    }, follow_redirects=True)
    return client

# Optional fixture: Add 7 days of HealthRecord data for dashboard
@pytest.fixture
def seed_health_data(app, test_user):
    base_date = date.today()
    for i in range(7):
        record = HealthRecord(
            user_id=test_user.id,
            date=base_date - timedelta(days=i),
            steps=8000 + i * 100,
            sleep_hours=6 + (i % 3),
            mood=(i % 5)
        )
        db.session.add(record)
    db.session.commit()
