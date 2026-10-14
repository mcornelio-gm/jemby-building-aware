"""
Unit & Integration Tests for Auth, Context-Cookie Persistence, and Network Portability.
"""

import os
import pytest
from fastapi.testclient import TestClient

from james_app.main import app
from james_app import auth


@pytest.fixture
def client():
    return TestClient(app)


def test_auth_credential_verification():
    """Verify built-in user authentication and password hashing."""
    user = auth.verify_credentials("engineer", "james123")
    assert user is not None
    assert user["username"] == "engineer"
    assert user["role"] == "engineer"

    admin = auth.verify_credentials("admin", "admin")
    assert admin is not None
    assert admin["role"] == "admin"

    bad = auth.verify_credentials("engineer", "wrongpassword")
    assert bad is None

    unknown = auth.verify_credentials("nonexistent", "password")
    assert unknown is None


def test_session_token_lifecycle():
    """Test cryptographic token creation, verification, and tamper resistance."""
    user_payload = {"username": "testuser", "name": "Tester", "role": "engineer"}
    token = auth.create_session_token(user_payload)
    assert token and "." in token

    decoded = auth.verify_session_token(token)
    assert decoded is not None
    assert decoded["username"] == "testuser"

    # Tampered token
    tampered = token[:-4] + "abcd"
    assert auth.verify_session_token(tampered) is None

    # Invalid token formats
    assert auth.verify_session_token("") is None
    assert auth.verify_session_token("invalid-format") is None


def test_root_redirect_default(client):
    """Test root redirect without cookies falls back to default demo facility."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/survey?client=zoetis&facility=b4"


def test_root_redirect_with_facility_cookies(client):
    """Test root redirect respects client and facility cookies."""
    cookies = {
        "james_last_client": "pfizer",
        "james_last_facility": "lab1",
        "james_last_view": "survey"
    }
    response = client.get("/", cookies=cookies, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/survey?client=pfizer&facility=lab1"


def test_root_redirect_with_sld_view_cookie(client):
    """Test root redirect respects SLD twin view preference."""
    cookies = {
        "james_last_client": "merck",
        "james_last_facility": "plant2",
        "james_last_view": "sld"
    }
    response = client.get("/", cookies=cookies, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/clients/merck/facilities/plant2/sld"


def test_root_redirect_with_last_url_cookie(client):
    """Test root redirect honors last visited URL cookie."""
    cookies = {
        "james_last_url": "/catalog?client=zoetis&facility=b4"
    }
    response = client.get("/", cookies=cookies, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/catalog?client=zoetis&facility=b4"


def test_survey_view_sets_context_cookies(client):
    """Test visiting /survey sets cookie headers for future session resumption."""
    response = client.get("/survey?client=abbott&facility=b1")
    assert response.status_code == 200
    assert "james_last_client=abbott" in response.headers.get("set-cookie", "")
    assert "james_last_facility=b1" in response.headers.get("set-cookie", "")
    assert "james_last_view=survey" in response.headers.get("set-cookie", "")


def test_login_flow(client):
    """Test login submission, token issuance, and logout."""
    # Failed login
    res_bad = client.post("/login", data={"username": "engineer", "password": "wrongpassword"})
    assert res_bad.status_code == 400

    # Successful login
    res_good = client.post("/login", data={"username": "engineer", "password": "james123"}, follow_redirects=False)
    assert res_good.status_code == 303
    assert auth.SESSION_COOKIE_NAME in res_good.headers.get("set-cookie", "")

    session_val = res_good.cookies.get(auth.SESSION_COOKIE_NAME)
    assert session_val is not None

    # Check API auth me with cookie
    client.cookies.set(auth.SESSION_COOKIE_NAME, session_val)
    res_me = client.get("/api/auth/me")
    assert res_me.status_code == 200
    data = res_me.json()
    assert data["authenticated"] is True
    assert data["user"]["username"] == "engineer"

    # Logout
    res_logout = client.get("/logout", follow_redirects=False)
    assert res_logout.status_code == 303
    assert res_logout.headers["location"] == "/login"

    # Verify GET /login renders the login page
    res_login_page = client.get("/login")
    assert res_login_page.status_code == 200
    assert "Sign In to Workbench" in res_login_page.text


def test_team_user_logins(client):
    """Test login for pre-seeded team members with email and username."""
    team_members = [
        ("benjie@jemby.com", "benjie", "admin"),
        ("mcornelio@jemby.com", "mcornelio", "admin"),
        ("stostado@jemby.com", "stostado", "engineer"),
        ("jcortes@jemby.com", "jcortes", "engineer"),
        ("benjie", "benjie", "admin"),
        ("mcornelio", "mcornelio", "admin")
    ]

    for identifier, password, expected_role in team_members:
        res = client.post("/login", data={"username": identifier, "password": password}, follow_redirects=False)
        assert res.status_code == 303, f"Failed login for {identifier}"
        session_val = res.cookies.get(auth.SESSION_COOKIE_NAME)
        assert session_val is not None, f"Missing session for {identifier}"

        # Verify profile returned from /api/auth/me
        client.cookies.set(auth.SESSION_COOKIE_NAME, session_val)
        res_me = client.get("/api/auth/me")
        assert res_me.status_code == 200
        user_info = res_me.json()["user"]
        assert user_info["role"] == expected_role


def test_api_users_list(client):
    """Test /api/users returns registered users list."""
    res = client.get("/api/users")
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 4
    emails = {u["email"] for u in users}
    assert "mcornelio@jemby.com" in emails
    assert "benjie@jemby.com" in emails
    assert "stostado@jemby.com" in emails
    assert "jcortes@jemby.com" in emails
