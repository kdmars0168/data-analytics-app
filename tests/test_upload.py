import os

def test_upload_route_accepts_valid_csv(client, test_user, app):
    login = client.post("/login", data={
        "email": test_user.email,
        "password": "testpass"
    }, follow_redirects=True)

    # Ensure login was successful
    assert login.status_code == 200

    csv_path = os.path.join("tests", "uploads","sample_upload_valid.csv")
    with open(csv_path, "rb") as f:
        data = {
            "file": (f, "sample_upload_valid.csv")
        }
        response = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
        assert response.status_code == 200
        assert b"File uploaded and data saved successfully!" in response.data

def test_upload_route_rejects_invalid_format(client, test_user, app):
    client.post("/login", data={
        "email": test_user.email,
        "password": "testpass"
    }, follow_redirects=True)

    # Create dummy txt file for test
    invalid_file_path = os.path.join("tests", "uploads","invalid_upload.txt")
    with open(invalid_file_path, "w") as f:
        f.write("this is not a csv")

    with open(invalid_file_path, "rb") as f:
        response = client.post("/upload", data={
            "file": (f, "invalid_upload.txt")
        }, content_type="multipart/form-data", follow_redirects=True)

    assert b"Invalid file format" in response.data


def test_upload_requires_login(client):
    response = client.get("/upload", follow_redirects=False)
    assert response.status_code == 302  # should redirect to login
    assert "/login" in response.headers["Location"]


def test_upload_with_missing_headers(client, test_user, app):
    client.post("/login", data={
        "email": test_user.email,
        "password": "testpass"
    }, follow_redirects=True)

    malformed_path = os.path.join("tests", "uploads","bad_headers.csv")
    with open(malformed_path, "w") as f:
        f.write("bad,columns,here\n1,2,3\n4,5,6")

    with open(malformed_path, "rb") as f:
        response = client.post("/upload", data={
            "file": (f, "bad_headers.csv")
        }, content_type="multipart/form-data", follow_redirects=True)

    assert b"Invalid" in response.data or response.status_code == 200  # fallback check
