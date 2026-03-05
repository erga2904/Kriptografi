"""
Auth Blueprint — registration, login, logout API.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.extensions import db
from app.models import User
from .services import validate_registration, validate_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    errors = validate_registration(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    user = User(
        username=data["username"].strip(),
        email=data["email"].strip().lower()
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({"ok": True, "user": user.username})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    errors, user = validate_login(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 401

    login_user(user)
    return jsonify({"ok": True, "user": user.username})


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True})
