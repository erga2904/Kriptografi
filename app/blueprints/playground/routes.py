"""
Playground API Routes — unified crypto sandbox.
"""
from flask import Blueprint, request, jsonify
from .services import run_playground, list_algorithms

playground_bp = Blueprint("playground", __name__)


@playground_bp.route("/run", methods=["POST"])
def run():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm", "")
    mode = data.get("mode", "encrypt")
    text = data.get("text", "")
    params = data.get("params", {})
    if not algorithm:
        return jsonify({"error": "Algoritma diperlukan."}), 400
    if not text and mode not in ("keygen",):
        return jsonify({"error": "Teks diperlukan."}), 400
    return jsonify(run_playground(algorithm, mode, text, params))


@playground_bp.route("/algorithms", methods=["GET"])
def algorithms():
    return jsonify(list_algorithms())
