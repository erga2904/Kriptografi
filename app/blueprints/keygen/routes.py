"""
Key Generator API Routes — RSA, AES, HMAC, random key generation.
"""
from flask import Blueprint, request, jsonify
from app.blueprints.keygen.services import (
    generate_rsa_keypair,
    generate_aes_key,
    generate_random_key,
    generate_hmac_key,
)

keygen_bp = Blueprint("keygen", __name__)


@keygen_bp.route("/rsa", methods=["POST"])
def rsa():
    data = request.get_json(silent=True) or {}
    bits = int(data.get("bits", 64))
    bits = max(16, min(bits, 1024))
    result = generate_rsa_keypair(bits)
    return jsonify(result)


@keygen_bp.route("/aes", methods=["POST"])
def aes():
    data = request.get_json(silent=True) or {}
    bits = int(data.get("bits", 256))
    if bits not in (128, 192, 256):
        bits = 256
    result = generate_aes_key(bits)
    return jsonify(result)


@keygen_bp.route("/random", methods=["POST"])
def random_key():
    data = request.get_json(silent=True) or {}
    length = int(data.get("length", 32))
    charset = data.get("charset", "hex")
    length = max(4, min(length, 256))
    result = generate_random_key(length, charset)
    return jsonify(result)


@keygen_bp.route("/hmac", methods=["POST"])
def hmac_key():
    data = request.get_json(silent=True) or {}
    bits = int(data.get("bits", 256))
    bits = max(128, min(bits, 512))
    result = generate_hmac_key(bits)
    return jsonify(result)
