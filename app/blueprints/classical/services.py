"""
Classical Cryptography Services
Caesar, Vigenere, Affine, Hill, Playfair — with step-by-step visualization.
"""
import math
import numpy as np

# ──────────────────────────── CAESAR ────────────────────────────

def caesar_encrypt(plaintext: str, shift: int) -> dict:
    shift = shift % 26
    steps = []
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            orig = ord(ch) - base
            shifted = (orig + shift) % 26
            new_ch = chr(base + shifted)
            steps.append({
                "char": ch,
                "original_pos": orig,
                "shift": shift,
                "formula": f"({orig} + {shift}) mod 26 = {shifted}",
                "result": new_ch
            })
            result.append(new_ch)
        else:
            steps.append({"char": ch, "result": ch, "formula": "non-alpha (unchanged)"})
            result.append(ch)
    return {
        "input": plaintext,
        "output": "".join(result),
        "shift": shift,
        "steps": steps,
        "math": f"E(x) = (x + {shift}) mod 26"
    }


def caesar_decrypt(ciphertext: str, shift: int) -> dict:
    shift = shift % 26
    steps = []
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            orig = ord(ch) - base
            shifted = (orig - shift) % 26
            new_ch = chr(base + shifted)
            steps.append({
                "char": ch,
                "original_pos": orig,
                "shift": shift,
                "formula": f"({orig} - {shift}) mod 26 = {shifted}",
                "result": new_ch
            })
            result.append(new_ch)
        else:
            steps.append({"char": ch, "result": ch, "formula": "non-alpha (unchanged)"})
            result.append(ch)
    return {
        "input": ciphertext,
        "output": "".join(result),
        "shift": shift,
        "steps": steps,
        "math": f"D(x) = (x - {shift}) mod 26"
    }


# ──────────────────────────── VIGENERE ────────────────────────────

def _extend_key(text: str, key: str) -> str:
    key = key.upper()
    extended = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            extended.append(key[ki % len(key)])
            ki += 1
        else:
            extended.append(ch)
    return "".join(extended)


def vigenere_encrypt(plaintext: str, key: str) -> dict:
    if not key or not key.isalpha():
        return {"error": "Key must contain only letters."}
    extended = _extend_key(plaintext, key)
    steps = []
    result = []
    for i, ch in enumerate(plaintext):
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch.upper()) - ord('A')
            k = ord(extended[i]) - ord('A')
            c = (p + k) % 26
            new_ch = chr(base + c) if ch.isupper() else chr(ord('a') + c)
            steps.append({
                "char": ch, "key_char": extended[i],
                "p": p, "k": k,
                "formula": f"({p} + {k}) mod 26 = {c}",
                "result": new_ch
            })
            result.append(new_ch)
        else:
            steps.append({"char": ch, "result": ch, "formula": "unchanged"})
            result.append(ch)
    return {
        "input": plaintext, "output": "".join(result),
        "key": key.upper(), "extended_key": extended,
        "steps": steps,
        "math": "E(pᵢ) = (pᵢ + kᵢ) mod 26"
    }


def vigenere_decrypt(ciphertext: str, key: str) -> dict:
    if not key or not key.isalpha():
        return {"error": "Key must contain only letters."}
    extended = _extend_key(ciphertext, key)
    steps = []
    result = []
    for i, ch in enumerate(ciphertext):
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch.upper()) - ord('A')
            k = ord(extended[i]) - ord('A')
            p = (c - k) % 26
            new_ch = chr(base + p) if ch.isupper() else chr(ord('a') + p)
            steps.append({
                "char": ch, "key_char": extended[i],
                "c": c, "k": k,
                "formula": f"({c} - {k}) mod 26 = {p}",
                "result": new_ch
            })
            result.append(new_ch)
        else:
            steps.append({"char": ch, "result": ch, "formula": "unchanged"})
            result.append(ch)
    return {
        "input": ciphertext, "output": "".join(result),
        "key": key.upper(), "extended_key": extended,
        "steps": steps,
        "math": "D(cᵢ) = (cᵢ - kᵢ) mod 26"
    }


# ──────────────────────────── AFFINE ────────────────────────────

def _mod_inverse(a: int, m: int):
    """Extended Euclidean to find modular inverse."""
    g, x, _ = _extended_gcd(a, m)
    if g != 1:
        return None
    return x % m


def _extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def affine_encrypt(plaintext: str, a: int, b: int) -> dict:
    if math.gcd(a, 26) != 1:
        return {"error": f"'a' ({a}) must be coprime with 26. gcd({a},26) = {math.gcd(a,26)}"}
    steps = []
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            x = ord(ch.upper()) - ord('A')
            c = (a * x + b) % 26
            new_ch = chr(base + c) if ch.isupper() else chr(ord('a') + c)
            steps.append({
                "char": ch, "x": x,
                "formula": f"({a}·{x} + {b}) mod 26 = {c}",
                "result": new_ch
            })
            result.append(new_ch)
        else:
            steps.append({"char": ch, "result": ch, "formula": "unchanged"})
            result.append(ch)
    return {
        "input": plaintext, "output": "".join(result),
        "a": a, "b": b,
        "steps": steps,
        "math": f"E(x) = ({a}·x + {b}) mod 26"
    }


def affine_decrypt(ciphertext: str, a: int, b: int) -> dict:
    if math.gcd(a, 26) != 1:
        return {"error": f"'a' ({a}) must be coprime with 26."}
    a_inv = _mod_inverse(a, 26)
    steps = []
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            y = ord(ch.upper()) - ord('A')
            p = (a_inv * (y - b)) % 26
            new_ch = chr(base + p) if ch.isupper() else chr(ord('a') + p)
            steps.append({
                "char": ch, "y": y,
                "formula": f"{a_inv}·({y} - {b}) mod 26 = {p}",
                "result": new_ch
            })
            result.append(new_ch)
        else:
            steps.append({"char": ch, "result": ch, "formula": "unchanged"})
            result.append(ch)
    return {
        "input": ciphertext, "output": "".join(result),
        "a": a, "b": b, "a_inv": a_inv,
        "steps": steps,
        "math": f"D(y) = {a_inv}·(y - {b}) mod 26"
    }


# ──────────────────────────── HILL ────────────────────────────

def _matrix_mod_inverse(matrix, mod):
    """Compute modular inverse of a 2×2 or 3×3 matrix mod n."""
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = _mod_inverse(det, mod)
    if det_inv is None:
        return None, f"Determinant ({det}) has no inverse mod {mod}."

    n = matrix.shape[0]
    if n == 2:
        adj = np.array([[matrix[1][1], -matrix[0][1]],
                         [-matrix[1][0], matrix[0][0]]])
    else:
        cofactor = np.zeros_like(matrix)
        for i in range(n):
            for j in range(n):
                minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                cofactor[i][j] = ((-1) ** (i + j)) * int(round(np.linalg.det(minor)))
        adj = cofactor.T

    inv = (det_inv * adj) % mod
    return inv.astype(int) % mod, None


def hill_encrypt(plaintext: str, key_matrix: list) -> dict:
    key = np.array(key_matrix, dtype=int)
    n = key.shape[0]
    text = "".join(ch.upper() for ch in plaintext if ch.isalpha())

    # Pad with X
    while len(text) % n != 0:
        text += "X"

    blocks = [text[i:i + n] for i in range(0, len(text), n)]
    steps = []
    result = []

    for block in blocks:
        vec = np.array([ord(c) - ord('A') for c in block], dtype=int)
        product = key.dot(vec) % 26
        enc_block = "".join(chr(v + ord('A')) for v in product)
        steps.append({
            "block": block,
            "vector": vec.tolist(),
            "key_matrix": key.tolist(),
            "product_raw": key.dot(vec).tolist(),
            "product_mod26": product.tolist(),
            "result": enc_block
        })
        result.append(enc_block)

    return {
        "input": plaintext, "processed": text,
        "output": "".join(result),
        "key_matrix": key.tolist(),
        "block_size": n,
        "steps": steps,
        "math": "C = K · P mod 26"
    }


def hill_decrypt(ciphertext: str, key_matrix: list) -> dict:
    key = np.array(key_matrix, dtype=int)
    inv_key, error = _matrix_mod_inverse(key, 26)
    if error:
        return {"error": error}

    n = key.shape[0]
    text = "".join(ch.upper() for ch in ciphertext if ch.isalpha())
    blocks = [text[i:i + n] for i in range(0, len(text), n)]
    steps = []
    result = []

    for block in blocks:
        vec = np.array([ord(c) - ord('A') for c in block], dtype=int)
        product = inv_key.dot(vec) % 26
        product = product.astype(int)
        dec_block = "".join(chr(int(v) + ord('A')) for v in product)
        steps.append({
            "block": block,
            "vector": vec.tolist(),
            "inv_key": inv_key.tolist(),
            "product_mod26": product.tolist(),
            "result": dec_block
        })
        result.append(dec_block)

    return {
        "input": ciphertext,
        "output": "".join(result),
        "key_matrix": key.tolist(),
        "inv_key_matrix": inv_key.tolist(),
        "steps": steps,
        "math": "P = K⁻¹ · C mod 26"
    }


# ──────────────────────────── PLAYFAIR ────────────────────────────

def _build_playfair_matrix(key: str):
    key = key.upper().replace("J", "I")
    seen = set()
    matrix_chars = []
    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            matrix_chars.append(ch)
    matrix = [matrix_chars[i:i + 5] for i in range(0, 25, 5)]
    return matrix, matrix_chars


def _find_pos(matrix, ch):
    ch = ch.upper()
    if ch == 'J':
        ch = 'I'
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    return None


def _prepare_playfair_pairs(text: str):
    text = text.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                pairs.append((a, 'X'))
                i += 1
            else:
                pairs.append((a, b))
                i += 2
        else:
            pairs.append((a, 'X'))
            i += 1
    return pairs


def playfair_encrypt(plaintext: str, key: str) -> dict:
    matrix, flat = _build_playfair_matrix(key)
    pairs = _prepare_playfair_pairs(plaintext)
    steps = []
    result = []

    for a, b in pairs:
        r1, c1 = _find_pos(matrix, a)
        r2, c2 = _find_pos(matrix, b)
        if r1 == r2:
            rule = "same row → shift right"
            ea = matrix[r1][(c1 + 1) % 5]
            eb = matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            rule = "same column → shift down"
            ea = matrix[(r1 + 1) % 5][c1]
            eb = matrix[(r2 + 1) % 5][c2]
        else:
            rule = "rectangle → swap columns"
            ea = matrix[r1][c2]
            eb = matrix[r2][c1]

        steps.append({
            "pair": f"{a}{b}",
            "pos_a": [r1, c1], "pos_b": [r2, c2],
            "rule": rule,
            "result": f"{ea}{eb}"
        })
        result.append(ea + eb)

    return {
        "input": plaintext,
        "output": "".join(result),
        "key": key.upper(),
        "matrix": matrix,
        "pairs": [f"{a}{b}" for a, b in pairs],
        "steps": steps,
        "math": "5×5 Polybius square substitution"
    }


def playfair_decrypt(ciphertext: str, key: str) -> dict:
    matrix, flat = _build_playfair_matrix(key)
    text = ciphertext.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())
    if len(text) % 2 != 0:
        text += "X"
    pairs = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
    steps = []
    result = []

    for a, b in pairs:
        r1, c1 = _find_pos(matrix, a)
        r2, c2 = _find_pos(matrix, b)
        if r1 == r2:
            rule = "same row → shift left"
            da = matrix[r1][(c1 - 1) % 5]
            db = matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            rule = "same column → shift up"
            da = matrix[(r1 - 1) % 5][c1]
            db = matrix[(r2 - 1) % 5][c2]
        else:
            rule = "rectangle → swap columns"
            da = matrix[r1][c2]
            db = matrix[r2][c1]

        steps.append({
            "pair": f"{a}{b}",
            "pos_a": [r1, c1], "pos_b": [r2, c2],
            "rule": rule,
            "result": f"{da}{db}"
        })
        result.append(da + db)

    return {
        "input": ciphertext,
        "output": "".join(result),
        "key": key.upper(),
        "matrix": matrix,
        "steps": steps,
        "math": "5×5 Polybius square reverse substitution"
    }
