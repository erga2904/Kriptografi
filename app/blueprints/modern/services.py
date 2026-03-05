"""
Modern Cryptography Services
AES, RSA, SHA-256, Digital Signature — with step visualization.
"""
import hashlib
import secrets
import math
from base64 import b64encode, b64decode


# ──────────────────────────── AES (simplified educational) ────────────────────────────

# S-Box for AES (first two rows shown, full 16×16)
AES_SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
]

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]


def _sub_bytes(state):
    return [AES_SBOX[b] for b in state]


def _shift_rows(state):
    """State is a flat list of 16 bytes, treated as 4×4 column-major."""
    m = [state[i:i+4] for i in range(0, 16, 4)]
    result = []
    for r in range(4):
        row = [m[c][r] for c in range(4)]
        shifted = row[r:] + row[:r]
        for c in range(4):
            m[c][r] = shifted[c]
    return [b for col in m for b in col]


def _xtime(a):
    return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else (a << 1) & 0xff


def _mix_single_column(col):
    t = col[0] ^ col[1] ^ col[2] ^ col[3]
    u = col[0]
    col[0] ^= _xtime(col[0] ^ col[1]) ^ t
    col[1] ^= _xtime(col[1] ^ col[2]) ^ t
    col[2] ^= _xtime(col[2] ^ col[3]) ^ t
    col[3] ^= _xtime(col[3] ^ u) ^ t
    return col


def _mix_columns(state):
    cols = [list(state[i:i+4]) for i in range(0, 16, 4)]
    mixed = []
    for col in cols:
        mixed.extend(_mix_single_column(col))
    return mixed


def _add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]


def _key_expansion_128(key_bytes):
    """AES-128 key expansion into 11 round keys."""
    w = list(key_bytes)
    for i in range(4, 44):
        temp = w[(i-1)*4:i*4]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [AES_SBOX[b] for b in temp]
            temp[0] ^= RCON[i//4 - 1]
        word_prev = w[(i-4)*4:(i-3)*4]
        new_word = [a ^ b for a, b in zip(word_prev, temp)]
        w.extend(new_word)
    return [w[i*16:(i+1)*16] for i in range(11)]


def aes_encrypt_demo(plaintext: str, key: str) -> dict:
    """Educational AES-128 single block encryption with step visualization."""
    # Pad key to 16 bytes
    key_bytes = key.encode('utf-8')[:16].ljust(16, b'\0')
    plain_bytes = plaintext.encode('utf-8')[:16].ljust(16, b'\0')

    round_keys = _key_expansion_128(key_bytes)
    state = list(plain_bytes)
    steps = []

    steps.append({
        "round": 0,
        "operation": "Initial AddRoundKey",
        "state_before": [f"{b:02x}" for b in state],
        "round_key": [f"{b:02x}" for b in round_keys[0]],
    })
    state = _add_round_key(state, round_keys[0])
    steps[-1]["state_after"] = [f"{b:02x}" for b in state]

    for r in range(1, 11):
        round_step = {"round": r, "operations": []}

        # SubBytes
        before = [f"{b:02x}" for b in state]
        state = _sub_bytes(state)
        round_step["operations"].append({
            "name": "SubBytes",
            "before": before,
            "after": [f"{b:02x}" for b in state]
        })

        # ShiftRows
        before = [f"{b:02x}" for b in state]
        state = _shift_rows(state)
        round_step["operations"].append({
            "name": "ShiftRows",
            "before": before,
            "after": [f"{b:02x}" for b in state]
        })

        # MixColumns (not in last round)
        if r < 10:
            before = [f"{b:02x}" for b in state]
            state = _mix_columns(state)
            round_step["operations"].append({
                "name": "MixColumns",
                "before": before,
                "after": [f"{b:02x}" for b in state]
            })

        # AddRoundKey
        before = [f"{b:02x}" for b in state]
        state = _add_round_key(state, round_keys[r])
        round_step["operations"].append({
            "name": "AddRoundKey",
            "round_key": [f"{b:02x}" for b in round_keys[r]],
            "before": before,
            "after": [f"{b:02x}" for b in state]
        })

        steps.append(round_step)

    ciphertext_hex = "".join(f"{b:02x}" for b in state)
    return {
        "input": plaintext,
        "output": ciphertext_hex,
        "key": key,
        "key_hex": key_bytes.hex(),
        "algorithm": "AES-128 (ECB, single block, educational)",
        "total_rounds": 10,
        "steps": steps,
        "math": "SubBytes → ShiftRows → MixColumns → AddRoundKey (×10 rounds)"
    }


# ──────────────────────────── RSA ────────────────────────────

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


def _mod_inverse(a, m):
    g, x, _ = _extended_gcd(a % m, m)
    if g != 1:
        return None
    return x % m


def rsa_generate_keys(bits=32) -> dict:
    """Generate RSA key pair with step-by-step visualization."""
    steps = []

    p = _generate_prime(bits)
    q = _generate_prime(bits)
    while q == p:
        q = _generate_prime(bits)

    steps.append({"step": "Generate primes", "p": p, "q": q})

    n = p * q
    steps.append({"step": "Compute n = p × q", "formula": f"{p} × {q} = {n}", "n": n})

    phi_n = (p - 1) * (q - 1)
    steps.append({
        "step": "Compute φ(n) = (p-1)(q-1)",
        "formula": f"({p}-1) × ({q}-1) = {phi_n}",
        "phi_n": phi_n
    })

    e = 65537
    if math.gcd(e, phi_n) != 1:
        e = 3
        while math.gcd(e, phi_n) != 1:
            e += 2

    steps.append({
        "step": "Choose e (coprime with φ(n))",
        "e": e,
        "gcd_check": f"gcd({e}, {phi_n}) = {math.gcd(e, phi_n)}"
    })

    d = _mod_inverse(e, phi_n)
    steps.append({
        "step": "Compute d = e⁻¹ mod φ(n)",
        "formula": f"d = {e}⁻¹ mod {phi_n} = {d}",
        "d": d,
        "verify": f"e × d mod φ(n) = {(e * d) % phi_n}"
    })

    return {
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
        "p": p, "q": q, "phi_n": phi_n,
        "steps": steps,
        "math": "RSA Key Generation: n=pq, φ(n)=(p-1)(q-1), ed≡1 mod φ(n)"
    }


def rsa_encrypt(plaintext: str, e: int, n: int) -> dict:
    steps = []
    encrypted = []
    for ch in plaintext:
        m = ord(ch)
        c = pow(m, e, n)
        steps.append({
            "char": ch,
            "m": m,
            "formula": f"{m}^{e} mod {n} = {c}",
            "c": c
        })
        encrypted.append(c)
    return {
        "input": plaintext,
        "output": encrypted,
        "output_str": " ".join(str(c) for c in encrypted),
        "public_key": {"e": e, "n": n},
        "steps": steps,
        "math": f"c = m^{e} mod {n}"
    }


def rsa_decrypt(ciphertext: list, d: int, n: int) -> dict:
    steps = []
    decrypted = []
    for c in ciphertext:
        c = int(c)
        m = pow(c, d, n)
        ch = chr(m) if 0 <= m < 1114112 else "?"
        steps.append({
            "c": c,
            "formula": f"{c}^{d} mod {n} = {m}",
            "m": m,
            "char": ch
        })
        decrypted.append(ch)
    return {
        "input": ciphertext,
        "output": "".join(decrypted),
        "private_key": {"d": d, "n": n},
        "steps": steps,
        "math": f"m = c^{d} mod {n}"
    }


# ──────────────────────────── SHA-256 ────────────────────────────

def sha256_hash(message: str) -> dict:
    """Compute SHA-256 with educational breakdown."""
    msg_bytes = message.encode('utf-8')
    digest = hashlib.sha256(msg_bytes).hexdigest()

    # Provide educational step info
    bit_len = len(msg_bytes) * 8
    padded_len = ((bit_len + 64) // 512 + 1) * 512
    num_blocks = padded_len // 512

    return {
        "input": message,
        "output": digest,
        "algorithm": "SHA-256",
        "steps": [
            {"step": "Input bytes", "value": msg_bytes.hex(), "length_bits": bit_len},
            {"step": "Padding", "description": f"Pad to {padded_len} bits ({num_blocks} block(s) of 512 bits)"},
            {"step": "Initial hash values (H0-H7)", "values": [
                "6a09e667", "bb67ae85", "3c6ef372", "a54ff53a",
                "510e527f", "9b05688c", "1f83d9ab", "5be0cd19"
            ]},
            {"step": "64 rounds of compression per block",
             "operations": "Ch, Maj, Σ0, Σ1, σ0, σ1 functions"},
            {"step": "Final hash", "value": digest}
        ],
        "math": "SHA-256: 64 rounds, 8 working variables, Merkle-Damgård construction"
    }


# ──────────────────────────── DIGITAL SIGNATURE ────────────────────────────

def digital_sign(message: str, bits=32) -> dict:
    """Simplified RSA digital signature demo."""
    keys = rsa_generate_keys(bits)
    d = keys["private_key"]["d"]
    n = keys["private_key"]["n"]
    e = keys["public_key"]["e"]

    msg_hash = hashlib.sha256(message.encode()).hexdigest()
    hash_int = int(msg_hash[:8], 16) % n  # Truncate for demo

    signature = pow(hash_int, d, n)
    verified_hash = pow(signature, e, n)
    is_valid = verified_hash == hash_int

    return {
        "message": message,
        "hash": msg_hash,
        "hash_truncated": hash_int,
        "signature": signature,
        "public_key": keys["public_key"],
        "private_key": keys["private_key"],
        "verification": {
            "recovered_hash": verified_hash,
            "original_hash": hash_int,
            "is_valid": is_valid
        },
        "steps": [
            {"step": "Hash message", "hash": msg_hash},
            {"step": "Truncate hash for demo", "value": hash_int},
            {"step": "Sign: s = hash^d mod n", "formula": f"{hash_int}^{d} mod {n} = {signature}"},
            {"step": "Verify: hash' = s^e mod n", "formula": f"{signature}^{e} mod {n} = {verified_hash}"},
            {"step": "Compare", "result": "VALID ✓" if is_valid else "INVALID ✗"}
        ],
        "key_generation": keys["steps"],
        "math": "Sign: s = H(m)^d mod n | Verify: H(m) ≟ s^e mod n"
    }
