
"""Security tests for SecureNotes API."""

from tests.conftest import login, auth


# ----- EXAMPLE: Missing token ---------------------------------------------
def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")
    assert res.status_code == 401


# ----- TODO 1: Invalid JWT ------------------------------------------------
def test_protected_route_rejects_bad_token(client):
    res = client.get(
        "/notes",
        headers=auth("not.a.jwt")
    )

    assert res.status_code == 401


# ----- TODO 2: Ownership protection --------------------------------------
def test_user_cannot_read_another_users_note(client):
    token = login(client, "alice", "alicepass")

    res = client.get(
        "/notes/2",
        headers=auth(token)
    )

    assert res.status_code == 403


# ----- TODO 3: Read own note ----------------------------------------------
def test_user_can_read_own_note(client):
    token = login(client, "alice", "alicepass")

    res = client.get(
        "/notes/1",
        headers=auth(token)
    )

    assert res.status_code == 200
    assert res.json()["title"] == "Alice diary"
    assert res.json()["owner_id"] == 2


# ----- TODO 4: Prevent username enumeration ------------------------------
def test_login_does_not_reveal_which_field_was_wrong(client):
    # Nonexistent user
    bad_user = client.post(
        "/login",
        json={
            "username": "unknownuser",
            "password": "somepassword"
        }
    )

    # Valid user, incorrect password
    bad_password = client.post(
        "/login",
        json={
            "username": "alice",
            "password": "wrongpassword"
        }
    )

    assert bad_user.status_code == 401
    assert bad_password.status_code == 401

    # Error responses must be identical
    assert bad_user.json() == bad_password.json()


# ----- TODO 5: Non-admin restriction -------------------------------------
def test_non_admin_cannot_list_users(client):
    token = login(client, "alice", "alicepass")

    res = client.get(
        "/admin/users",
        headers=auth(token)
    )

    assert res.status_code == 403


# ----- TODO 6: Prevent password disclosure -------------------------------
def test_admin_can_list_users_without_password_leak(client):
    token = login(client, "admin", "admin123")

    res = client.get(
        "/admin/users",
        headers=auth(token)
    )

    assert res.status_code == 200

    users = res.json()

    assert isinstance(users, list)
    assert len(users) > 0

    # Only approved user fields should be returned
    for user in users:
        assert set(user.keys()) == {
            "id",
            "username",
            "is_admin"
        }
        assert "password" not in user
