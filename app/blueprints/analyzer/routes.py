"""
Analyzer API Routes — cipher detection and entropy analysis.
"""
from flask import Blueprint, request, jsonify
from .services import detect_cipher, entropy_analysis

analyzer_bp = Blueprint("analyzer", __name__)


@analyzer_bp.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Teks diperlukan."}), 400
    return jsonify(detect_cipher(text))


@analyzer_bp.route("/entropy", methods=["POST"])
def entropy():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    encrypted = data.get("encrypted_text")
    if not text:
        return jsonify({"error": "Teks diperlukan."}), 400
    return jsonify(entropy_analysis(text, encrypted))
