"""
JAMES Structured JSON Audit Logging Module.

Provides enterprise-grade JSON logging for all user and system actions
using python-json-logger. Captures user email, roles, IP addresses,
facility context, and operation payloads for auditing and GCP Cloud Logging.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from pythonjsonlogger import json as jsonlogger

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("JAMES_DATA_DIR", str(BASE_DIR / "data")))
AUDIT_LOG_FILE = DATA_DIR / "audit.jsonl"


def _setup_audit_logger() -> logging.Logger:
    """Configure structured JSON logger with file and stdout handlers."""
    logger = logging.getLogger("james.audit")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Avoid duplicate handlers on reload
    if logger.handlers:
        return logger

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Standard JSON log record format
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(action)s %(user_email)s %(message)s"
    )

    # 1. Stdout handler (auto-parsed by Google Cloud Logging on Cloud Run)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # 2. File handler (local persistent JSONL log)
    file_handler = logging.FileHandler(AUDIT_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


audit_logger = _setup_audit_logger()


def log_audit(
    action: str,
    user: Optional[Dict[str, Any]] = None,
    client_id: Optional[str] = None,
    facility_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Any] = None,
    level: str = "INFO",
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log an auditable structured JSON event.

    Args:
        action: Auditable action verb (e.g. 'USER_LOGIN', 'EQUIPMENT_CREATE', 'SLD_MUTATION')
        user: Active user dictionary (containing 'email', 'username', 'role')
        client_id: Client workspace identifier (e.g. 'zoetis')
        facility_id: Facility workspace identifier (e.g. 'b4')
        resource_type: Target domain/resource (e.g. 'equipment', 'feeder', 'catalog')
        resource_id: Tag or identifier of mutated item (e.g. 'MDP-1')
        details: Extra operational metadata dictionary
        request: FastAPI Request object to extract client IP and user agent
        level: Log level ('INFO', 'WARNING', 'ERROR')
        message: Human readable summary
    """
    user_dict = user or {}
    user_email = user_dict.get("email") or user_dict.get("username") or "anonymous"
    user_name = user_dict.get("name") or user_email
    user_role = user_dict.get("role") or "viewer"

    # Extract client IP and user agent if request is provided
    ip_address = None
    user_agent = None
    if request:
        client_host = getattr(request, "client", None)
        ip_address = request.headers.get("x-forwarded-for", client_host.host if client_host else None)
        user_agent = request.headers.get("user-agent")

    log_payload = {
        "action": action,
        "user_email": user_email,
        "user_name": user_name,
        "user_role": user_role,
        "client_id": client_id,
        "facility_id": facility_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "details": details or {},
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    msg = message or f"[{action}] User {user_email} performed {action}"
    if resource_id:
        msg += f" on {resource_type or 'resource'} '{resource_id}'"
    if facility_id:
        msg += f" in {client_id or 'client'}/{facility_id}"

    # Log with extra structured attributes
    lvl = getattr(logging, level.upper(), logging.INFO)
    audit_logger.log(lvl, msg, extra=log_payload)

    return log_payload


def get_recent_audit_logs(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve recent structured audit log records from persistent file."""
    if not AUDIT_LOG_FILE.exists():
        return []

    logs = []
    try:
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines[-limit:]):
                line = line.strip()
                if line:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        audit_logger.error("Failed to read audit log file", extra={"error": str(e)})

    return logs
