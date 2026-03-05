"""
Classical Cryptography API Routes
"""
from flask import Blueprint, request, jsonify
from .services import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    hill_encrypt, hill_decrypt,
    playfair_encrypt, playfair_decrypt
)

classical_bp = Blueprint("classical", __name__)


@classical_bp.route("/caesar", methods=["POST"])
def caesar():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    shift = int(data.get("shift", 3))
    mode = data.get("mode", "encrypt")
    if not text:
        return jsonify({"error": "Text is required."}), 400
    fn = caesar_encrypt if mode == "encrypt" else caesar_decrypt
    return jsonify(fn(text, shift))


@classical_bp.route("/vigenere", methods=["POST"])
def vigenere():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    key = data.get("key", "")
    mode = data.get("mode", "encrypt")
    if not text or not key:
        return jsonify({"error": "Text and key are required."}), 400
    fn = vigenere_encrypt if mode == "encrypt" else vigenere_decrypt
    result = fn(text, key)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@classical_bp.route("/affine", methods=["POST"])
def affine():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    a = int(data.get("a", 5))
    b = int(data.get("b", 8))
    mode = data.get("mode", "encrypt")
    if not text:
        return jsonify({"error": "Text is required."}), 400
    fn = affine_encrypt if mode == "encrypt" else affine_decrypt
    result = fn(text, a, b)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@classical_bp.route("/hill", methods=["POST"])
def hill():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    key_matrix = data.get("key_matrix", [[6, 24, 1], [13, 16, 10], [20, 17, 15]])
    mode = data.get("mode", "encrypt")
    if not text:
        return jsonify({"error": "Text is required."}), 400
    fn = hill_encrypt if mode == "encrypt" else hill_decrypt
    result = fn(text, key_matrix)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@classical_bp.route("/playfair", methods=["POST"])
def playfair():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    key = data.get("key", "")
    mode = data.get("mode", "encrypt")
    if not text or not key:
        return jsonify({"error": "Text and key are required."}), 400
    fn = playfair_encrypt if mode == "encrypt" else playfair_decrypt
    result = fn(text, key)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)
