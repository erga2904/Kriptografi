"""
Modern Cryptography API Routes
"""
from flask import Blueprint, request, jsonify
from .services import (
    aes_encrypt_demo,
    rsa_generate_keys, rsa_encrypt, rsa_decrypt,
    sha256_hash, digital_sign
)

modern_bp = Blueprint("modern", __name__)


@modern_bp.route("/aes", methods=["POST"])
def aes():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    key = data.get("key", "")
    if not text or not key:
        return jsonify({"error": "Text and key are required."}), 400
    return jsonify(aes_encrypt_demo(text, key))


@modern_bp.route("/rsa/keygen", methods=["POST"])
def rsa_keygen():
    data = request.get_json(silent=True) or {}
    bits = int(data.get("bits", 32))
    bits = min(max(bits, 16), 64)
    return jsonify(rsa_generate_keys(bits))


@modern_bp.route("/rsa/encrypt", methods=["POST"])
def rsa_enc():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    e = int(data.get("e", 65537))
    n = int(data.get("n", 0))
    if not text or not n:
        return jsonify({"error": "Text, e, and n are required."}), 400
    return jsonify(rsa_encrypt(text, e, n))


@modern_bp.route("/rsa/decrypt", methods=["POST"])
def rsa_dec():
    data = request.get_json(silent=True) or {}
    ciphertext = data.get("ciphertext", [])
    d = int(data.get("d", 0))
    n = int(data.get("n", 0))
    if not ciphertext or not d or not n:
        return jsonify({"error": "Ciphertext, d, and n are required."}), 400
    return jsonify(rsa_decrypt(ciphertext, d, n))


@modern_bp.route("/sha256", methods=["POST"])
def sha256():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required."}), 400
    return jsonify(sha256_hash(text))


@modern_bp.route("/signature", methods=["POST"])
def signature():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message is required."}), 400
    bits = int(data.get("bits", 32))
    return jsonify(digital_sign(message, bits))
