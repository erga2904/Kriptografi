"""
Math Tools API Routes
"""
from flask import Blueprint, request, jsonify
from .services import (
    modular_arithmetic,
    euclidean_algorithm,
    extended_euclidean,
    modular_inverse,
    fast_exponentiation
)

math_bp = Blueprint("math_tools", __name__)


@math_bp.route("/modular", methods=["POST"])
def modular():
    data = request.get_json(silent=True) or {}
    a = int(data.get("a", 0))
    b = int(data.get("b", 0))
    mod = int(data.get("mod", 26))
    operation = data.get("operation", "add")
    if mod == 0:
        return jsonify({"error": "Modulus cannot be zero."}), 400
    return jsonify(modular_arithmetic(a, b, mod, operation))


@math_bp.route("/euclidean", methods=["POST"])
def euclidean():
    data = request.get_json(silent=True) or {}
    a = int(data.get("a", 0))
    b = int(data.get("b", 0))
    return jsonify(euclidean_algorithm(a, b))


@math_bp.route("/extended-euclidean", methods=["POST"])
def ext_euclidean():
    data = request.get_json(silent=True) or {}
    a = int(data.get("a", 0))
    b = int(data.get("b", 0))
    return jsonify(extended_euclidean(a, b))


@math_bp.route("/mod-inverse", methods=["POST"])
def mod_inverse():
    data = request.get_json(silent=True) or {}
    a = int(data.get("a", 0))
    m = int(data.get("m", 26))
    if m == 0:
        return jsonify({"error": "Modulus cannot be zero."}), 400
    return jsonify(modular_inverse(a, m))


@math_bp.route("/fast-exp", methods=["POST"])
def fast_exp():
    data = request.get_json(silent=True) or {}
    base = int(data.get("base", 2))
    exp = int(data.get("exp", 10))
    mod = int(data.get("mod", 1000))
    if mod == 0:
        return jsonify({"error": "Modulus cannot be zero."}), 400
    return jsonify(fast_exponentiation(base, exp, mod))
