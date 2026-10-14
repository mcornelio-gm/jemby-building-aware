"""
JAMES Multi-Tenant Authentication & Session Management Module.

Provides session-cookie verification, persistent user store integration,
and Google OAuth 2.0 / OpenID Connect SSO integration.
"""

import os
import hmac
import hashlib
import json
import base64
import time
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse

from james_app.users import (
    verify_user_credentials,
    create_or_update_google_user,
    get_user_by_identifier,
    list_users
)

# Secret key for HMAC signing session tokens
AUTH_SECRET_KEY = os.getenv("JAMES_AUTH_SECRET", "james-building-aware-secret-key-2026-default")
SESSION_COOKIE_NAME = "james_session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 7  # 7 days

# Configurable Auth enforcement flag
AUTH_ENABLED = os.getenv("JAMES_AUTH_ENABLED", "false").lower() in ("true", "1", "yes")

# Google OAuth 2.0 Credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")


def hash_password(password: str) -> str:
    """Hash password with SHA-256 for local verification."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_credentials(identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """Verify username/email and password against persistent user store."""
    return verify_user_credentials(identifier, password)


def create_session_token(user_data: Dict[str, Any]) -> str:
    """Create a signed, base64-encoded session payload."""
    payload = {
        "user": user_data,
        "exp": int(time.time()) + SESSION_MAX_AGE_SECONDS,
        "iat": int(time.time())
    }
    payload_json = json.dumps(payload, separators=(",", ":"))
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode("utf-8")).decode("utf-8")
    signature = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return f"{payload_b64}.{signature}"


def verify_session_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
    """Verify cryptographic signature and expiration of session token."""
    if not token or "." not in token:
        return None
    try:
        payload_b64, signature = token.split(".", 1)
        expected_sig = hmac.new(
            AUTH_SECRET_KEY.encode("utf-8"),
            payload_b64.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        
        payload_json = base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode("utf-8")
        payload = json.loads(payload_json)
        
        if payload.get("exp", 0) < time.time():
            return None
        return payload.get("user")
    except Exception:
        return None


def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """FastAPI Dependency: Extract current active user from session cookie or return None."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    user = verify_session_token(token)
    if user:
        return user
    if not AUTH_ENABLED:
        # Default active administrator identity when AUTH_ENABLED is False (development mode)
        return {
            "username": "admin",
            "email": "admin@buildingaware.io",
            "name": "System Administrator",
            "role": "admin",
            "is_guest": False
        }
    return None


def require_authenticated_user(request: Request) -> Dict[str, Any]:
    """FastAPI Dependency: Require authenticated user, raising 401 or redirecting to /login."""
    user = get_current_user(request)
    if not user or (AUTH_ENABLED and user.get("is_guest")):
        # Check if this is an API request or HTML browser navigation
        accept = request.headers.get("accept", "")
        if "text/html" in accept:
            # HTML request - redirect to login
            raise HTTPException(
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                headers={"Location": f"/login?next={request.url.path}"}
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return user


def require_admin_user(request: Request) -> Dict[str, Any]:
    """FastAPI Dependency: Require authenticated user with admin role."""
    user = require_authenticated_user(request)
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to perform this action."
        )
    return user


# ---------------------------------------------------------------------------
# Google OAuth 2.0 / OpenID Connect SSO Integration
# ---------------------------------------------------------------------------

def is_google_sso_configured() -> bool:
    """Check if Google OAuth2 environment variables are active."""
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def get_google_auth_url(redirect_uri: str, state: str = "") -> str:
    """Generate Google OAuth 2.0 consent screen redirect URL."""
    if not is_google_sso_configured():
        return "#"
    scope = "openid%20email%20profile"
    return (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"redirect_uri={urllib.parse.quote(redirect_uri, safe='')}&"
        f"state={urllib.parse.quote(state, safe='')}&"
        f"access_type=offline&"
        f"prompt=select_account"
    )


def exchange_google_code_for_user(code: str, redirect_uri: str) -> Optional[Dict[str, Any]]:
    """Exchange authorization code for user profile and auto-provision in user database."""
    if not is_google_sso_configured():
        return None
    try:
        # 1. Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        payload = urllib.parse.urlencode({
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }).encode("utf-8")

        req = urllib.request.Request(token_url, data=payload, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        with urllib.request.urlopen(req, timeout=10) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))

        access_token = token_data.get("access_token")
        if not access_token:
            return None

        # 2. Fetch user profile info
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_req = urllib.request.Request(userinfo_url)
        user_req.add_header("Authorization", f"Bearer {access_token}")

        with urllib.request.urlopen(user_req, timeout=10) as user_resp:
            profile = json.loads(user_resp.read().decode("utf-8"))

        email = profile.get("email")
        if not email:
            return None

        google_id = profile.get("sub", "")
        name = profile.get("name", email.split("@")[0])
        picture = profile.get("picture")

        # Provision or link in persistent user store
        return create_or_update_google_user(
            email=email,
            google_id=google_id,
            name=name,
            avatar_url=picture
        )
    except Exception as e:
        print(f"Error during Google OAuth exchange: {e}")
        return None
