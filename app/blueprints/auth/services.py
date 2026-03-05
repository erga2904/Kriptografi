"""
Auth Service — validation helpers.
"""
import re
from app.models import User


def validate_registration(data: dict) -> list[str]:
    errors = []
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if len(username) < 3:
        errors.append("Username must be at least 3 characters.")
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        errors.append("Invalid email address.")
    if len(password) < 6:
        errors.append("Password must be at least 6 characters.")
    if User.query.filter_by(username=username).first():
        errors.append("Username already taken.")
    if User.query.filter_by(email=email).first():
        errors.append("Email already registered.")
    return errors


def validate_login(data: dict):
    errors = []
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        errors.append("Invalid email or password.")
        return errors, None
    return errors, user
