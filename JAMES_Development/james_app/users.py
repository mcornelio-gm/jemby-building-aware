"""
JAMES Persistent User Management and Authentication Store.

Provides multi-tenant user storage, role-based permissions, secure password hashing,
and Google SSO user auto-provisioning. Backed by persistent JSON/SQLite store.
"""

import os
import json
import sqlite3
import hashlib
import hmac
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("JAMES_DATA_DIR", str(BASE_DIR / "data")))
USERS_FILE = DATA_DIR / "users.json"
USERS_DB = DATA_DIR / "users.db"


class User(BaseModel):
    """User account model for JAMES Digital Twin."""
    id: str
    email: str
    username: str
    name: str
    role: str = "engineer"  # 'admin', 'engineer', 'surveyor', 'viewer'
    password_hash: str
    password_salt: str = ""
    google_id: Optional[str] = None
    avatar_url: Optional[str] = None
    client_access: List[str] = Field(default_factory=lambda: ["*"])
    is_active: bool = True
    created_at: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    last_login_at: Optional[str] = None


def hash_password(password: str, salt: str = "") -> str:
    """Hash password with SHA-256 and optional salt."""
    salted = f"{salt}{password}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


# Initial seeded user profiles (passwords default to part before @ as requested)
INITIAL_USERS: List[Dict[str, Any]] = [
    {
        "id": "usr_benjie",
        "email": "benjie@jemby.com",
        "username": "benjie",
        "name": "Benjie",
        "role": "admin",
        "password": "benjie",
        "client_access": ["*"]
    },
    {
        "id": "usr_mcornelio",
        "email": "mcornelio@jemby.com",
        "username": "mcornelio",
        "name": "Michael Cornelio",
        "role": "admin",
        "password": "mcornelio",
        "client_access": ["*"]
    },
    {
        "id": "usr_stostado",
        "email": "stostado@jemby.com",
        "username": "stostado",
        "name": "S. Tostado",
        "role": "engineer",
        "password": "stostado",
        "client_access": ["*"]
    },
    {
        "id": "usr_jcortes",
        "email": "jcortes@jemby.com",
        "username": "jcortes",
        "name": "J. Cortes",
        "role": "engineer",
        "password": "jcortes",
        "client_access": ["*"]
    },
    # Backwards-compatible system aliases for automated test suites
    {
        "id": "usr_admin",
        "email": "admin@buildingaware.io",
        "username": "admin",
        "name": "System Administrator",
        "role": "admin",
        "password": "admin",
        "client_access": ["*"]
    },
    {
        "id": "usr_engineer",
        "email": "engineer@buildingaware.io",
        "username": "engineer",
        "name": "Electrical Engineer",
        "role": "engineer",
        "password": "james123",
        "client_access": ["*"]
    },
    {
        "id": "usr_demo",
        "email": "demo@buildingaware.io",
        "username": "demo",
        "name": "Demo User",
        "role": "viewer",
        "password": "demo",
        "client_access": ["*"]
    }
]


def ensure_users_db() -> None:
    """Ensure data directory and persistent SQLite user database exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(USERS_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'engineer',
                password_hash TEXT NOT NULL,
                password_salt TEXT DEFAULT '',
                google_id TEXT,
                avatar_url TEXT,
                client_access TEXT DEFAULT '["*"]',
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                last_login_at TEXT
            )
        """)
        conn.commit()


def seed_default_users() -> None:
    """Seed initial team users if database or json file is empty."""
    ensure_users_db()
    existing = list_users()
    existing_emails = {u.email.lower() for u in existing}
    existing_usernames = {u.username.lower() for u in existing}

    for init in INITIAL_USERS:
        email = init["email"].lower()
        username = init["username"].lower()
        if email not in existing_emails and username not in existing_usernames:
            salt = os.urandom(8).hex()
            pwd_hash = hash_password(init["password"], salt)
            user = User(
                id=init["id"],
                email=email,
                username=username,
                name=init["name"],
                role=init["role"],
                password_hash=pwd_hash,
                password_salt=salt,
                client_access=init.get("client_access", ["*"]),
                is_active=True
            )
            save_user(user)


def save_user(user: User) -> None:
    """Save or update user in SQLite and companion JSON store."""
    ensure_users_db()
    with sqlite3.connect(USERS_DB) as conn:
        conn.execute("""
            INSERT INTO users (
                id, email, username, name, role, password_hash, password_salt,
                google_id, avatar_url, client_access, is_active, created_at, last_login_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                email=excluded.email,
                username=excluded.username,
                name=excluded.name,
                role=excluded.role,
                password_hash=excluded.password_hash,
                password_salt=excluded.password_salt,
                google_id=excluded.google_id,
                avatar_url=excluded.avatar_url,
                client_access=excluded.client_access,
                is_active=excluded.is_active,
                last_login_at=excluded.last_login_at
        """, (
            user.id,
            user.email.lower(),
            user.username.lower(),
            user.name,
            user.role,
            user.password_hash,
            user.password_salt,
            user.google_id,
            user.avatar_url,
            json.dumps(user.client_access),
            1 if user.is_active else 0,
            user.created_at,
            user.last_login_at
        ))
        conn.commit()

    # Sync to JSON file for portable Git backups
    _sync_users_to_json()


def list_users() -> List[User]:
    """Retrieve all users from SQLite."""
    ensure_users_db()
    with sqlite3.connect(USERS_DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM users ORDER BY created_at ASC").fetchall()
        users = []
        for r in rows:
            users.append(User(
                id=r["id"],
                email=r["email"],
                username=r["username"],
                name=r["name"],
                role=r["role"],
                password_hash=r["password_hash"],
                password_salt=r["password_salt"] or "",
                google_id=r["google_id"],
                avatar_url=r["avatar_url"],
                client_access=json.loads(r["client_access"]) if r["client_access"] else ["*"],
                is_active=bool(r["is_active"]),
                created_at=r["created_at"],
                last_login_at=r["last_login_at"]
            ))
        return users


def _sync_users_to_json() -> None:
    """Dump all users to users.json for human-readable state inspection and sync to GCS."""
    users = list_users()
    data = [u.model_dump() for u in users]
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    try:
        from james_app.gcs_sync import sync_file_to_gcs_async
        sync_file_to_gcs_async(USERS_DB)
        sync_file_to_gcs_async(USERS_FILE)
    except Exception:
        pass


def get_user_by_identifier(identifier: str) -> Optional[User]:
    """Find user by email or username (case-insensitive)."""
    ensure_users_db()
    clean = identifier.strip().lower()
    with sqlite3.connect(USERS_DB) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM users WHERE LOWER(email) = ? OR LOWER(username) = ? LIMIT 1",
            (clean, clean)
        ).fetchone()
        if not row:
            return None
        return User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            name=row["name"],
            role=row["role"],
            password_hash=row["password_hash"],
            password_salt=row["password_salt"] or "",
            google_id=row["google_id"],
            avatar_url=row["avatar_url"],
            client_access=json.loads(row["client_access"]) if row["client_access"] else ["*"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
            last_login_at=row["last_login_at"]
        )


def get_user_by_google_id(google_id: str) -> Optional[User]:
    """Find user by linked Google account ID."""
    ensure_users_db()
    with sqlite3.connect(USERS_DB) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM users WHERE google_id = ? LIMIT 1", (google_id,)).fetchone()
        if not row:
            return None
        return User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            name=row["name"],
            role=row["role"],
            password_hash=row["password_hash"],
            password_salt=row["password_salt"] or "",
            google_id=row["google_id"],
            avatar_url=row["avatar_url"],
            client_access=json.loads(row["client_access"]) if row["client_access"] else ["*"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
            last_login_at=row["last_login_at"]
        )


def verify_user_credentials(identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """Verify username/email and password against persistent user store."""
    seed_default_users()
    user = get_user_by_identifier(identifier)
    if not user or not user.is_active:
        return None

    # Verify with salt
    computed_hash = hash_password(password, user.password_salt)
    # Also support unsalted SHA-256 legacy check
    legacy_hash = hash_password(password, "")

    if hmac.compare_digest(user.password_hash, computed_hash) or hmac.compare_digest(user.password_hash, legacy_hash):
        # Update last login timestamp
        user.last_login_at = time.strftime("%Y-%m-%d %H:%M:%S")
        save_user(user)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "avatar_url": user.avatar_url,
            "client_access": user.client_access
        }

    return None


def create_or_update_google_user(email: str, google_id: str, name: str, avatar_url: Optional[str] = None) -> Dict[str, Any]:
    """Link or auto-provision a Google SSO authenticated user."""
    seed_default_users()
    clean_email = email.strip().lower()
    user = get_user_by_identifier(clean_email) or get_user_by_google_id(google_id)

    if user:
        # Link Google ID and update avatar
        user.google_id = google_id
        if avatar_url and not user.avatar_url:
            user.avatar_url = avatar_url
        user.last_login_at = time.strftime("%Y-%m-%d %H:%M:%S")
        save_user(user)
    else:
        # Auto-provision new user with username from email prefix
        prefix = clean_email.split("@")[0]
        user = User(
            id=f"usr_{prefix}_{int(time.time())}",
            email=clean_email,
            username=prefix,
            name=name or prefix,
            role="engineer",
            password_hash=hash_password(prefix, ""),
            google_id=google_id,
            avatar_url=avatar_url,
            client_access=["*"],
            is_active=True,
            last_login_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        save_user(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "avatar_url": user.avatar_url,
        "client_access": user.client_access
    }


def admin_reset_user_password(identifier: str, new_password: str) -> bool:
    """Admin utility to set or reset a user's password."""
    ensure_users_db()
    user = get_user_by_identifier(identifier)
    if not user:
        return False
    salt = os.urandom(8).hex()
    user.password_salt = salt
    user.password_hash = hash_password(new_password, salt)
    save_user(user)
    return True


def admin_upsert_user(
    email: str,
    name: str,
    role: str = "engineer",
    initial_password: Optional[str] = None,
    is_active: bool = True
) -> User:
    """Admin utility to create or update a user account."""
    ensure_users_db()
    clean_email = email.strip().lower()
    user = get_user_by_identifier(clean_email)
    prefix = clean_email.split("@")[0]

    if user:
        user.name = name.strip() or user.name
        user.role = role
        user.is_active = is_active
        if initial_password and initial_password.strip():
            salt = os.urandom(8).hex()
            user.password_salt = salt
            user.password_hash = hash_password(initial_password.strip(), salt)
        save_user(user)
        return user
    else:
        salt = os.urandom(8).hex()
        pwd = initial_password.strip() if initial_password and initial_password.strip() else prefix
        pwd_hash = hash_password(pwd, salt)
        user = User(
            id=f"usr_{prefix}_{int(time.time())}",
            email=clean_email,
            username=prefix,
            name=name.strip() or prefix,
            role=role,
            password_hash=pwd_hash,
            password_salt=salt,
            client_access=["*"],
            is_active=is_active
        )
        save_user(user)
        return user


def admin_delete_user(identifier: str) -> bool:
    """Admin utility to permanently delete a user from SQLite and companion JSON."""
    ensure_users_db()
    user = get_user_by_identifier(identifier)
    if not user:
        return False
    with sqlite3.connect(USERS_DB) as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user.id,))
        conn.commit()
    _sync_users_to_json()
    return True


def admin_toggle_user_active(identifier: str, is_active: bool) -> bool:
    """Admin utility to activate/deactivate a user account."""
    ensure_users_db()
    user = get_user_by_identifier(identifier)
    if not user:
        return False
    user.is_active = is_active
    save_user(user)
    return True


# Automatically seed on module import
seed_default_users()

