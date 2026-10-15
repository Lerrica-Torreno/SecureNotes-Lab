
"""API behaviour tests for SecureNotes."""

from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1: Register and login -----------------------------------------
def test_register_then_login(client):
    # Register a new user
    register_res = client.post(
        "/register",
        json={
            "username": "charlie",
            "password": "charliepass"
        }
    )

    assert register_res.status_code == 200

    # Log in using the newly registered account
    login_res = client.post(
        "/login",
        json={
            "username": "charlie",
            "password": "charliepass"
        }
    )

    assert login_res.status_code == 200

    token = login_res.json()["access_token"]

    # A JWT must contain three dot-separated parts
    assert token.count(".") == 2
    assert login_res.json()["token_type"] == "bearer"


# ----- TODO 2: Wrong password ---------------------------------------------
def test_login_wrong_password_is_401(client):
    res = client.post(
        "/login",
        json={
            "username": "alice",
            "password": "wrongpassword"
        }
    )

    assert res.status_code == 401


# ----- TODO 3: Create and list own note -----------------------------------
def test_create_then_list_own_note(client):
    # Log in as Alice
    token = login(client, "alice", "alicepass")

    # Create a new note
    create_res = client.post(
        "/notes",
        headers=auth(token),
        json={
            "title": "My Test Note",
            "body": "This is a test note."
        }
    )

    assert create_res.status_code == 200
    assert create_res.json()["title"] == "My Test Note"

    # Retrieve Alice's notes
    list_res = client.get(
        "/notes",
        headers=auth(token)
    )

    assert list_res.status_code == 200

    notes = list_res.json()

    # Verify the newly created note exists
    assert any(
        note["title"] == "My Test Note"
        for note in notes
    )
