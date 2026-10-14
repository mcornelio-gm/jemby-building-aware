"""Unit tests for structured JSON audit logging with python-json-logger."""

import json
from fastapi.testclient import TestClient
from james_app.main import app
from james_app.audit_logger import log_audit, get_recent_audit_logs, AUDIT_LOG_FILE
from james_app import auth


def test_direct_log_audit():
    """Test manual log_audit emission and structured JSON fields."""
    user = {
        "email": "mcornelio@jemby.com",
        "username": "mcornelio",
        "name": "Michael Cornelio",
        "role": "admin"
    }

    event = log_audit(
        action="TEST_ACTION",
        user=user,
        client_id="zoetis",
        facility_id="b4",
        resource_type="equipment",
        resource_id="MDP-1",
        details={"test_key": "test_val"}
    )

    assert event["action"] == "TEST_ACTION"
    assert event["user_email"] == "mcornelio@jemby.com"
    assert event["user_role"] == "admin"
    assert event["client_id"] == "zoetis"
    assert event["facility_id"] == "b4"
    assert event["resource_id"] == "MDP-1"
    assert "timestamp_iso" in event

    # Verify log is written to JSONL file
    recent = get_recent_audit_logs(limit=10)
    assert any(log.get("action") == "TEST_ACTION" and log.get("user_email") == "mcornelio@jemby.com" for log in recent)


def test_login_audit_trail():
    """Test that authenticating via /login records a structured JSON audit event."""
    client = TestClient(app)

    # Perform login
    res = client.post(
        "/login",
        data={"username": "mcornelio@jemby.com", "password": "mcornelio"},
        follow_redirects=False
    )
    assert res.status_code == 303

    # Check recent logs
    recent = get_recent_audit_logs(limit=20)
    login_events = [
        log for log in recent
        if log.get("action") == "USER_LOGIN_SUCCESS" and log.get("user_email") == "mcornelio@jemby.com"
    ]
    assert len(login_events) > 0
    assert login_events[0]["user_name"] == "Michael Cornelio"


def test_api_audit_logs_endpoint():
    """Test GET /api/audit-logs endpoint."""
    client = TestClient(app)
    res = client.get("/api/audit-logs?limit=5")
    assert res.status_code == 200
    logs = res.json()
    assert isinstance(logs, list)
