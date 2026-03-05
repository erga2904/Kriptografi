"""
Attack Simulation API Routes
"""
from flask import Blueprint, request, jsonify
from .services import brute_force_caesar, frequency_analysis, rsa_weak_key_attack

attacks_bp = Blueprint("attacks", __name__)


@attacks_bp.route("/brute-caesar", methods=["POST"])
def brute_caesar():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Ciphertext is required."}), 400
    return jsonify(brute_force_caesar(text))


@attacks_bp.route("/frequency", methods=["POST"])
def frequency():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required."}), 400
    result = frequency_analysis(text)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@attacks_bp.route("/rsa-weak", methods=["POST"])
def rsa_weak():
    data = request.get_json(silent=True) or {}
    n = int(data.get("n", 0))
    e = int(data.get("e", 65537))
    if n < 4:
        return jsonify({"error": "n must be at least 4."}), 400
    return jsonify(rsa_weak_key_attack(n, e))
