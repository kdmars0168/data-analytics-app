import pytest
from datetime import date

# Utility for logging in test user
def login_test_user(client, test_user):
    return client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)

def test_submit_manual_valid(client, test_user, app):
    login_test_user(client, test_user)
    response = client.post("/submit_manual", data={
        "date": date.today().strftime("%Y-%m-%d"),
        "steps": "7500",
        "sleep": "7.5",
        "mood": "Happy"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Manual data submitted successfully!" in response.data

def test_submit_manual_missing_field(client, test_user):
    login_test_user(client, test_user)
    response = client.post("/submit_manual", data={
        "date": date.today().strftime("%Y-%m-%d"),
        "steps": "7000",
        "sleep": "6.5",
        # mood is missing
    }, follow_redirects=True)
    assert response.status_code == 400 or b"error" in response.data.lower()

def test_submit_manual_invalid_data(client, test_user):
    login_test_user(client, test_user)
    response = client.post("/submit_manual", data={
        "date": "not-a-date",
        "steps": "seven thousand",
        "sleep": "ten",
        "mood": "Excited"  # not in mood map
    }, follow_redirects=True)
    assert response.status_code == 400 or b"error" in response.data.lower()