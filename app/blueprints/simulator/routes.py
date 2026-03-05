"""
Simulator API Routes — uses modern RSA keygen for visual simulation.
"""
from flask import Blueprint, request, jsonify
from app.blueprints.modern.services import rsa_generate_keys

simulator_bp = Blueprint("simulator", __name__)


@simulator_bp.route("/rsa-visual", methods=["POST"])
def rsa_visual():
    data = request.get_json(silent=True) or {}
    p = data.get("p")
    q = data.get("q")

    if p and q:
        p, q = int(p), int(q)
        # Manual computation with provided p, q
        import math
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = 65537
        if math.gcd(e, phi_n) != 1:
            e = 3
            while math.gcd(e, phi_n) != 1:
                e += 2

        def _ext_gcd(a, b):
            if a == 0: return b, 0, 1
            g, x1, y1 = _ext_gcd(b % a, a)
            return g, y1 - (b // a) * x1, x1

        g, x, _ = _ext_gcd(e % phi_n, phi_n)
        d = x % phi_n if g == 1 else None

        # Primality check
        def is_prime_simple(n):
            if n < 2: return False
            for i in range(2, min(int(n**0.5) + 1, 100000)):
                if n % i == 0: return False
            return True

        steps = [
            {"step": "Input prima", "p": p, "q": q,
             "p_is_prime": is_prime_simple(p), "q_is_prime": is_prime_simple(q)},
            {"step": "Hitung n = p × q", "formula": f"{p} × {q} = {n}"},
            {"step": "Hitung φ(n) = (p-1)(q-1)", "formula": f"({p}-1) × ({q}-1) = {phi_n}"},
            {"step": "Pilih e (koprima dengan φ(n))", "e": e,
             "formula": f"gcd({e}, {phi_n}) = {math.gcd(e, phi_n)}"},
            {"step": "Hitung d = e⁻¹ mod φ(n)", "formula": f"d = {d}",
             "verify": f"{e} × {d} mod {phi_n} = {(e * d) % phi_n}" if d else "Tidak ada"},
        ]

        return jsonify({
            "p": p, "q": q, "n": n, "phi_n": phi_n,
            "public_key": {"e": e, "n": n},
            "private_key": {"d": d, "n": n},
            "steps": steps,
            "valid": is_prime_simple(p) and is_prime_simple(q) and d is not None
        })
    else:
        bits = int(data.get("bits", 16))
        return jsonify(rsa_generate_keys(bits))
