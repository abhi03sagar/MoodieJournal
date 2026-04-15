from werkzeug.security import generate_password_hash, check_password_hash
from Modules.database.mongo_client import create_user, authenticate_user


def _is_valid_email(email):
    if not isinstance(email, str):
        return False
    email = email.strip()
    return "@" in email and "." in email and len(email) >= 5


def _sanitize_registration(username, email, password):
    if not isinstance(username, str) or not username.strip():
        return None, "Username is required."
    if not _is_valid_email(email):
        return None, "A valid email is required."
    if not isinstance(password, str) or len(password) < 8:
        return None, "Password must be at least 8 characters long."

    return {
        "username": username.strip(),
        "email": email.strip().lower(),
        "password": password
    }, None


def _sanitize_login(username, email, password):
    normalized_username = username.strip() if isinstance(username, str) else ""
    normalized_email = email.strip().lower() if isinstance(email, str) else ""

    if not normalized_username and not normalized_email:
        return None, "Provide username or email."

    if normalized_email and not _is_valid_email(normalized_email):
        return None, "A valid email is required."

    if not isinstance(password, str) or len(password) < 8:
        return None, "Password must be at least 8 characters long."

    return {
        "username": normalized_username,
        "email": normalized_email,
        "password": password
    }, None


def register_user(username, email, password):
    sanitized, error = _sanitize_registration(username, email, password)
    if error:
        return {"ok": False, "error": error}

    password_hash = generate_password_hash(sanitized["password"], method="pbkdf2:sha256")
    result = create_user(sanitized["username"], sanitized["email"], password_hash)

    if not result["ok"]:
        return result

    return {
        "ok": True,
        "message": "User registered successfully.",
        "user_id": result["user_id"]
    }


def login_user(username, email, password):
    sanitized, error = _sanitize_login(username, email, password)
    if error:
        return {"ok": False, "error": error}

    user = authenticate_user(sanitized["username"], sanitized["email"])
    if user is None:
        return {"ok": False, "error": "Invalid credentials."}

    if not check_password_hash(user["password_hash"], sanitized["password"]):
        return {"ok": False, "error": "Invalid credentials."}

    return {
        "ok": True,
        "message": "Login successful.",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
    }
