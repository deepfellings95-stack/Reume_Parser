import secrets
from flask import session, request, abort

CSRF_SESSION_KEY = "_csrf_token"


def generate_csrf_token():
    """Create & store CSRF token in session"""
    if CSRF_SESSION_KEY not in session:
        session[CSRF_SESSION_KEY] = secrets.token_urlsafe(32)
    return session[CSRF_SESSION_KEY]


def validate_csrf():
    """Validate CSRF token from form or header"""
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        session_token = session.get(CSRF_SESSION_KEY)
        if not session_token:
            abort(403, "Missing CSRF session token")

        # Accept token from form OR header (React)
        request_token = (
            request.form.get("csrf_token")
            or request.headers.get("X-CSRF-Token")
        )

        if not request_token or request_token != session_token:
            abort(403, "Invalid CSRF token")
