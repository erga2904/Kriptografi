"""
Key Generator Service — generate various cryptographic keys.
"""
import secrets
import string
import math
import hashlib


def _is_prime(n, k=20):
    """Miller-Rabin primality test."""
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _generate_prime(bits=32):
    while True:
        n = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if _is_prime(n):
            return n


def _extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def generate_rsa_keypair(bits: int = 512) -> dict:
    """Generate RSA key pair."""
    bits = max(16, min(bits, 1024))
    half = bits // 2

    p = _generate_prime(half)
    q = _generate_prime(half)
    while q == p:
        q = _generate_prime(half)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi_n) != 1:
        e = 3
        while math.gcd(e, phi_n) != 1:
            e += 2

    g, x, _ = _extended_gcd(e % phi_n, phi_n)
    d = x % phi_n

    actual_bits = n.bit_length()

    return {
        "type": "RSA",
        "bits": actual_bits,
        "e": e,
        "n": str(n),
        "d": str(d),
        "p": str(p),
        "q": str(q),
        "phi_n": str(phi_n),
        "public_key": {"e": e, "n": str(n)},
        "private_key": {"d": str(d), "n": str(n)}
    }


def generate_aes_key(bits: int = 256) -> dict:
    """Generate random AES key."""
    bits = max(128, min(bits, 256))
    # Round to valid AES key size
    if bits <= 128:
        bits = 128
    elif bits <= 192:
        bits = 192
    else:
        bits = 256

    key_bytes = secrets.token_bytes(bits // 8)
    iv_bytes = secrets.token_bytes(16)

    return {
        "type": "AES",
        "bits": bits,
        "bytes": bits // 8,
        "hex": key_bytes.hex(),
        "base64": __import__('base64').b64encode(key_bytes).decode(),
        "key_hex": key_bytes.hex(),
        "key_base64": __import__('base64').b64encode(key_bytes).decode(),
        "iv_hex": iv_bytes.hex(),
        "iv_base64": __import__('base64').b64encode(iv_bytes).decode()
    }


def generate_random_key(length: int = 32, charset: str = "all") -> dict:
    """Generate random cryptographic key/password."""
    length = max(8, min(length, 256))
    symbol_space = 0

    if charset == "hex":
        chars = string.hexdigits[:16]
        key = ''.join(secrets.choice(chars) for _ in range(length))
        symbol_space = len(chars)
    elif charset == "alphanumeric":
        chars = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(chars) for _ in range(length))
        symbol_space = len(chars)
    elif charset == "alphabetic":
        chars = string.ascii_letters
        key = ''.join(secrets.choice(chars) for _ in range(length))
        symbol_space = len(chars)
    elif charset == "numeric":
        key = ''.join(str(secrets.randbelow(10)) for _ in range(length))
        symbol_space = 10
    else:  # all
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        key = ''.join(secrets.choice(chars) for _ in range(length))
        symbol_space = len(chars)

    # Calculate entropy
    entropy_per_char = math.log2(symbol_space)
    total_entropy = round(entropy_per_char * length, 1)

    key_bytes = key.encode('utf-8')

    return {
        "type": "Random Key",
        "key": key,
        "length": length,
        "charset": charset,
        "hex": key_bytes.hex(),
        "base64": __import__('base64').b64encode(key_bytes).decode(),
        "sha256_hash": hashlib.sha256(key_bytes).hexdigest(),
        "entropy_bits": total_entropy,
        "strength": "Sangat Kuat" if total_entropy > 128 else
                    "Kuat" if total_entropy > 80 else
                    "Sedang" if total_entropy > 50 else "Lemah"
    }


def generate_hmac_key(bits: int = 256) -> dict:
    """Generate HMAC key."""
    bits = max(128, min(bits, 512))
    key_bytes = secrets.token_bytes(bits // 8)

    return {
        "type": "HMAC",
        "bits": bits,
        "bytes": bits // 8,
        "hex": key_bytes.hex(),
        "base64": __import__('base64').b64encode(key_bytes).decode(),
        "key_hex": key_bytes.hex(),
        "key_base64": __import__('base64').b64encode(key_bytes).decode(),
        "length_bytes": bits // 8,
        "strength": "Kriptografis Kuat"
    }
