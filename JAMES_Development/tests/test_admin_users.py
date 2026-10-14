"""
Unit tests for JAMES Admin User Management and Password Reset Console.
"""

import pytest
from fastapi.testclient import TestClient
from james_app.main import app
from james_app import auth
from james_app.users import (
    get_user_by_identifier,
    verify_user_credentials,
    admin_reset_user_password,
    admin_upsert_user,
    admin_delete_user,
    admin_toggle_user_active
)


@pytest.fixture
def admin_client():
    client = TestClient(app)
    # Login as admin benjie
    client.post("/login", data={"username": "benjie@jemby.com", "password": "benjie"})
    return client


@pytest.fixture
def engineer_client():
    client = TestClient(app)
    # Login as engineer stostado
    client.post("/login", data={"username": "stostado@jemby.com", "password": "stostado"})
    return client


def test_admin_list_users_authorized(admin_client):
    response = admin_client.get("/api/admin/users")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["users"]) >= 4
    emails = [u["email"] for u in data["users"]]
    assert "benjie@jemby.com" in emails
    assert "mcornelio@jemby.com" in emails


def test_admin_list_users_forbidden_for_engineer(engineer_client):
    response = engineer_client.get("/api/admin/users")
    assert response.status_code == 403


def test_admin_password_reset_flow(admin_client):
    # Reset password for jcortes
    new_pwd = "JembyReset2026!"
    response = admin_client.post(
        "/api/admin/users/reset-password",
        json={"identifier": "jcortes@jemby.com", "new_password": new_pwd}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify old password fails
    assert verify_user_credentials("jcortes@jemby.com", "jcortes") is None

    # Verify new password succeeds
    user_auth = verify_user_credentials("jcortes@jemby.com", new_pwd)
    assert user_auth is not None
    assert user_auth["email"] == "jcortes@jemby.com"

    # Reset back to jcortes
    admin_reset_user_password("jcortes@jemby.com", "jcortes")
    assert verify_user_credentials("jcortes@jemby.com", "jcortes") is not None


def test_admin_upsert_and_delete_user(admin_client):
    test_email = "test_user_temporary@jemby.com"
    # 1. Create user
    res = admin_client.post(
        "/api/admin/users/upsert",
        json={
            "email": test_email,
            "name": "Temporary Test User",
            "role": "surveyor",
            "password": "TempPassword123!",
            "is_active": True
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["user"]["email"] == test_email
    assert data["user"]["role"] == "surveyor"

    # Verify authentication works
    auth_res = verify_user_credentials(test_email, "TempPassword123!")
    assert auth_res is not None

    # 2. Toggle active
    toggle_res = admin_client.post(
        "/api/admin/users/toggle-active",
        json={"identifier": test_email, "is_active": False}
    )
    assert toggle_res.status_code == 200
    assert verify_user_credentials(test_email, "TempPassword123!") is None

    # 3. Delete user
    del_res = admin_client.post(
        "/api/admin/users/delete",
        json={"identifier": test_email}
    )
    assert del_res.status_code == 200
    assert get_user_by_identifier(test_email) is None


def test_admin_cannot_delete_self(admin_client):
    res = admin_client.post(
        "/api/admin/users/delete",
        json={"identifier": "benjie@jemby.com"}
    )
    assert res.status_code == 400
    assert "cannot delete your own" in res.json()["detail"]
