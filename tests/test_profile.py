import pytest

def login_test_user(client, test_user):
    client.post('/login', data={
        'email': test_user.email,
        'password': 'testpass'
    }, follow_redirects=True)

def test_profile_requires_login(client):
    response = client.get('/profile')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_profile_page_renders(client, test_user):
    login_test_user(client, test_user)
    response = client.get('/profile')
    assert response.status_code == 200
    assert b"Profile" in response.data
    assert test_user.name.encode() in response.data

def test_edit_profile_success(client, test_user):
    login_test_user(client, test_user)
    
    response = client.post('/profile', data={
        "name": "Updated Name",
        "gender": "other",
        "dob": "1991-05-20",
        "height": "180",
        "weight": "75",
        "medical_conditions": "Updated Condition"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Profile updated successfully" in response.data
    assert b"Updated Name" in response.data
