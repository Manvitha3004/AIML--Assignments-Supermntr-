""" Assignment - 7th Feb 2026
strong code for password authentication using Python 

"""

import hashlib
import hmac
import os
import re
import time
from datetime import datetime, timedelta

# ── Storage (in-memory for demo; swap for a real DB in production) ──────────
_users: dict = {}          # username -> {salt, hash, failed_attempts, locked_until}
_sessions: dict = {}       # token -> {username, expires_at}

# ── Config ────
MAX_FAILED   = 5
LOCKOUT_SECS = 300          # 5 minutes
SESSION_MINS = 30
MIN_PWD_LEN  = 12

# ── Helpers ─────
def _hash_password(password: str, salt: bytes) -> bytes:
    """PBKDF2-HMAC-SHA256 — slow by design to resist brute-force."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations=600_000,    # NIST 2024 recommendation
    )

def _validate_strength(password: str) -> list[str]:
    """Returns a list of unmet requirements (empty = strong enough)."""
    issues = []
    if len(password) < MIN_PWD_LEN:
        issues.append(f"at least {MIN_PWD_LEN} characters")
    if not re.search(r"[A-Z]", password):
        issues.append("one uppercase letter")
    if not re.search(r"[a-z]", password):
        issues.append("one lowercase letter")
    if not re.search(r"\d", password):
        issues.append("one digit")
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        issues.append("one special character")
    return issues

# ── Core API ────
def register(username: str, password: str) -> dict:
    """Register a new user. Returns {ok, message}."""
    username = username.strip().lower()

    if not username or len(username) < 3:
        return {"ok": False, "message": "Username must be at least 3 characters."}
    if username in _users:
        return {"ok": False, "message": "Username already exists."}

    issues = _validate_strength(password)
    if issues:
        return {"ok": False, "message": "Password needs: " + ", ".join(issues) + "."}

    salt = os.urandom(32)
    _users[username] = {
        "salt": salt,
        "hash": _hash_password(password, salt),
        "failed_attempts": 0,
        "locked_until": None,
    }
    return {"ok": True, "message": f"User '{username}' registered successfully."}


def login(username: str, password: str) -> dict:
    """Authenticate a user. Returns {ok, message, token?}."""
    username = username.strip().lower()
    user = _users.get(username)

    # Always do a dummy compare to prevent timing-based user enumeration
    dummy_salt = os.urandom(32)
    dummy_hash = _hash_password("dummy", dummy_salt)

    if not user:
        hmac.compare_digest(_hash_password(password, dummy_salt), dummy_hash)
        return {"ok": False, "message": "Invalid username or password."}

    # Lockout check
    if user["locked_until"] and datetime.utcnow() < user["locked_until"]:
        remaining = int((user["locked_until"] - datetime.utcnow()).total_seconds())
        return {"ok": False, "message": f"Account locked. Try again in {remaining}s."}

    # Constant-time comparison
    expected = user["hash"]
    actual   = _hash_password(password, user["salt"])
    if not hmac.compare_digest(expected, actual):
        user["failed_attempts"] += 1
        if user["failed_attempts"] >= MAX_FAILED:
            user["locked_until"] = datetime.utcnow() + timedelta(seconds=LOCKOUT_SECS)
            return {"ok": False, "message": f"Too many failed attempts. Account locked for {LOCKOUT_SECS}s."}
        left = MAX_FAILED - user["failed_attempts"]
        return {"ok": False, "message": f"Invalid username or password. {left} attempt(s) left."}

    # Success — reset counters, issue session token
    user["failed_attempts"] = 0
    user["locked_until"]    = None

    token = hmac.new(os.urandom(32), os.urandom(32), "sha256").hexdigest()
    _sessions[token] = {
        "username":   username,
        "expires_at": datetime.utcnow() + timedelta(minutes=SESSION_MINS),
    }
    return {"ok": True, "message": "Login successful.", "token": token}


def verify_session(token: str) -> dict:
    """Check whether a session token is still valid."""
    session = _sessions.get(token)
    if not session:
        return {"ok": False, "message": "Invalid session."}
    if datetime.utcnow() > session["expires_at"]:
        del _sessions[token]
        return {"ok": False, "message": "Session expired."}
    return {"ok": True, "username": session["username"]}


def logout(token: str) -> dict:
    """Invalidate a session token."""
    if _sessions.pop(token, None):
        return {"ok": True, "message": "Logged out."}
    return {"ok": False, "message": "Token not found."}


def change_password(username: str, old_password: str, new_password: str) -> dict:
    """Change password after verifying the current one."""
    auth = login(username, old_password)
    if not auth["ok"]:
        return auth                            # Reuse lockout / error logic

    issues = _validate_strength(new_password)
    if issues:
        return {"ok": False, "message": "New password needs: " + ", ".join(issues) + "."}
    if old_password == new_password:
        return {"ok": False, "message": "New password must differ from the current one."}

    user      = _users[username.strip().lower()]
    salt      = os.urandom(32)
    user["salt"] = salt
    user["hash"] = _hash_password(new_password, salt)

    # Revoke all existing sessions for this user
    for tok in [t for t, s in _sessions.items() if s["username"] == username]:
        del _sessions[tok]

    return {"ok": True, "message": "Password changed successfully. Please log in again."}

if __name__ == "__main__":
    print("=== Registration ===")
    print(register("alice", "Weak"))                         # fail — too weak
    print(register("alice", "Str0ng!P@ssword#1"))            # ok
    print(register("alice", "Str0ng!P@ssword#1"))            # fail — duplicate

    print("\n=== Login ===")
    print(login("alice", "wrongpassword"))                   # fail
    result = login("alice", "Str0ng!P@ssword#1")             # ok
    print(result)
    token = result.get("token")

    print("\n=== Session Verification ===")
    print(verify_session(token))                             # ok
    print(verify_session("fake-token"))                      # fail

    print("\n=== Brute-Force Lockout ===")
    for _ in range(6):
        print(login("alice", "badpassword"))

    print("\n=== Change Password ===")
    # Re-register a fresh user to demo password change
    register("bob", "Str0ng!P@ssword#1")
    print(change_password("bob", "Str0ng!P@ssword#1", "Str0ng!P@ssword#1"))  # same — fail
    print(change_password("bob", "Str0ng!P@ssword#1", "N3wP@ssw0rd!XYZ"))    # ok

    print("\n=== Logout ===")
    print(logout(token))
    print(verify_session(token))                             # expired


""" breakdown of every security layer built into this code:
Hashing & Salting

PBKDF2-HMAC-SHA256 with 600,000 iterations (NIST 2024 recommendation) — makes brute-force attacks extremely slow
A random 32-byte salt per user prevents rainbow table attacks

Timing Attack Prevention

hmac.compare_digest() for constant-time hash comparison — no early-exit leaking info
A dummy hash computation is done even for non-existent usernames, preventing user enumeration via response timing

Brute-Force Protection

Accounts lock after 5 failed attempts for 300 seconds
Remaining attempts are shown to the user

Session Management

Tokens generated from hmac over two os.urandom() values — cryptographically strong
Sessions expire after 30 minutes
All sessions are revoked on password change

Password Strength Enforcement

Minimum 12 characters, requires uppercase, lowercase, digit, and special character """