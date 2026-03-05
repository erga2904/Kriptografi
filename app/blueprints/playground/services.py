"""
Playground Service — unified interface to all cipher algorithms.
"""
import time
from typing import Any, Dict
from app.blueprints.classical.services import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    hill_encrypt, hill_decrypt,
    playfair_encrypt, playfair_decrypt
)
from app.blueprints.modern.services import (
    aes_encrypt_demo, rsa_generate_keys, rsa_encrypt, rsa_decrypt,
    sha256_hash, digital_sign
)


ALGORITHMS = {
    "caesar": {
        "name": "Caesar Cipher",
        "type": "classical",
        "params": ["shift"],
        "supports": ["encrypt", "decrypt"]
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "type": "classical",
        "params": ["key"],
        "supports": ["encrypt", "decrypt"]
    },
    "affine": {
        "name": "Affine Cipher",
        "type": "classical",
        "params": ["a", "b"],
        "supports": ["encrypt", "decrypt"]
    },
    "hill": {
        "name": "Hill Cipher",
        "type": "classical",
        "params": ["key_matrix"],
        "supports": ["encrypt", "decrypt"]
    },
    "playfair": {
        "name": "Playfair Cipher",
        "type": "classical",
        "params": ["key"],
        "supports": ["encrypt", "decrypt"]
    },
    "aes": {
        "name": "AES-128",
        "type": "modern",
        "params": ["key"],
        "supports": ["encrypt"]
    },
    "rsa": {
        "name": "RSA",
        "type": "modern",
        "params": ["bits"],
        "supports": ["keygen", "encrypt", "decrypt"]
    },
    "sha256": {
        "name": "SHA-256",
        "type": "modern",
        "params": [],
        "supports": ["hash"]
    }
}


def list_algorithms():
    return ALGORITHMS


def run_playground(algorithm: str, mode: str, text: str, params: dict) -> dict:
    """Execute a cipher algorithm and return result with timing."""
    start = time.perf_counter()
    result: Dict[str, Any] = {}

    try:
        if algorithm == "caesar":
            shift = int(params.get("shift", 3))
            fn = caesar_encrypt if mode == "encrypt" else caesar_decrypt
            data = fn(text, shift)
            result["result"] = data.get("output", data) if isinstance(data, dict) else data
            result["steps"] = data.get("steps", []) if isinstance(data, dict) else []

        elif algorithm == "vigenere":
            key = params.get("key", "SECRET")
            fn = vigenere_encrypt if mode == "encrypt" else vigenere_decrypt
            data = fn(text, key)
            result["result"] = data.get("output", data) if isinstance(data, dict) else data
            result["steps"] = data.get("steps", []) if isinstance(data, dict) else []

        elif algorithm == "affine":
            a = int(params.get("a", 5))
            b = int(params.get("b", 8))
            fn = affine_encrypt if mode == "encrypt" else affine_decrypt
            data = fn(text, a, b)
            result["result"] = data.get("output", data) if isinstance(data, dict) else data
            result["steps"] = data.get("steps", []) if isinstance(data, dict) else []

        elif algorithm == "hill":
            key_matrix = params.get("key_matrix", [[6, 24, 1], [13, 16, 10], [20, 17, 15]])
            fn = hill_encrypt if mode == "encrypt" else hill_decrypt
            data = fn(text, key_matrix)
            result["result"] = data.get("output", data) if isinstance(data, dict) else data
            result["steps"] = data.get("steps", []) if isinstance(data, dict) else []

        elif algorithm == "playfair":
            key = params.get("key", "MONARCHY")
            fn = playfair_encrypt if mode == "encrypt" else playfair_decrypt
            data = fn(text, key)
            result["result"] = data.get("output", data) if isinstance(data, dict) else data
            result["steps"] = data.get("steps", []) if isinstance(data, dict) else []

        elif algorithm == "aes":
            key = params.get("key", "MySecretKey12345")
            data = aes_encrypt_demo(text, key)
            result["result"] = data.get("output", data) if isinstance(data, dict) else data
            result["steps"] = data.get("steps", []) if isinstance(data, dict) else []

        elif algorithm == "rsa":
            if mode == "keygen":
                bits = int(params.get("bits", 32))
                data = rsa_generate_keys(bits)
                result["result"] = str(data)
                result["steps"] = []
            elif mode == "encrypt":
                e = int(params.get("e", 65537))
                n = int(params.get("n", 0))
                data = rsa_encrypt(text, e, n)
                result["result"] = data.get("output_str", data) if isinstance(data, dict) else str(data)
                result["steps"] = []
            elif mode == "decrypt":
                d = int(params.get("d", 0))
                n = int(params.get("n", 0))
                ciphertext = params.get("ciphertext", [])
                data = rsa_decrypt(ciphertext, d, n)
                result["result"] = data.get("output", data) if isinstance(data, dict) else str(data)
                result["steps"] = []

        elif algorithm == "sha256":
            data = sha256_hash(text)
            result["result"] = data.get("hash", data) if isinstance(data, dict) else str(data)
            result["steps"] = []

        else:
            result = {"error": f"Algoritma tidak dikenal: {algorithm}"}

    except Exception as e:
        result = {"error": str(e)}

    elapsed = time.perf_counter() - start
    
    # Return with frontend-expected keys
    return {
        "result": result.get("result", ""),
        "steps": result.get("steps", []),
        "time_ms": round(elapsed * 1000, 3),
        "output_length": len(str(result.get("result", ""))),
        "algorithm": ALGORITHMS.get(algorithm, {}).get("name", algorithm),
        "mode": mode,
        "error": result.get("error")
    } if "error" not in result else {"error": result.get("error")}
