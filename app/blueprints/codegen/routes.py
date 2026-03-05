"""
Code Generator API Routes — generate algorithm implementations in various languages.
"""
from flask import Blueprint, request, jsonify
from app.blueprints.codegen.services import generate_code, get_available_algorithms

codegen_bp = Blueprint("codegen", __name__)


@codegen_bp.route("/algorithms", methods=["GET"])
def algorithms():
    return jsonify(get_available_algorithms())


@codegen_bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm", "caesar")
    language = data.get("language", "python")

    result = generate_code(algorithm, language)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)
