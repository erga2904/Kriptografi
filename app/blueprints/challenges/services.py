"""
Challenge Service — generate crypto challenges with scoring.
"""
import random
import hashlib
import time
from app.blueprints.classical.services import (
    caesar_encrypt, vigenere_encrypt, affine_encrypt
)


# ──────────────────── Challenge Definitions ────────────────────

CHALLENGES = {
    # Easy challenges
    "caesar_easy_1": {
        "id": "caesar_easy_1",
        "title": "Dekripsi Pesan Caesar",
        "description": "Sebuah pesan dienkripsi menggunakan Caesar Cipher. Tentukan isi pesan aslinya!",
        "difficulty": "mudah",
        "points": 100,
        "type": "dekripsi",
        "cipher": "caesar",
        "hints": [
            "Coba semua kemungkinan pergeseran (0-25)",
            "Pergeseran yang digunakan adalah angka satu digit",
            "Pergeseran = {shift}"
        ]
    },
    "caesar_easy_2": {
        "id": "caesar_easy_2",
        "title": "Temukan Kunci Caesar",
        "description": "Kamu tahu bahwa plaintext = '{plain_hint}...' dan ciphertext diberikan. Temukan nilai pergeseran!",
        "difficulty": "mudah",
        "points": 100,
        "type": "temukan_kunci",
        "cipher": "caesar",
        "hints": [
            "Bandingkan huruf pertama plaintext dan ciphertext",
            "Pergeseran = (huruf_cipher - huruf_plain) mod 26",
            "Jawabannya adalah {shift}"
        ]
    },
    # Medium challenges
    "vigenere_medium_1": {
        "id": "vigenere_medium_1",
        "title": "Pecahkan Vigenère",
        "description": "Pesan dienkripsi dengan Vigenère Cipher. Kunci terdiri dari 3-4 huruf umum.",
        "difficulty": "sedang",
        "points": 250,
        "type": "dekripsi",
        "cipher": "vigenere",
        "hints": [
            "Gunakan analisis frekuensi untuk menemukan panjang kunci",
            "Panjang kunci adalah {key_len} huruf",
            "Kunci dimulai dengan '{key_start}'"
        ]
    },
    "affine_medium_1": {
        "id": "affine_medium_1",
        "title": "Pecahkan Affine Cipher",
        "description": "Pesan dienkripsi dengan Affine Cipher E(x) = (ax + b) mod 26. Temukan pesan aslinya!",
        "difficulty": "sedang",
        "points": 250,
        "type": "dekripsi",
        "cipher": "affine",
        "hints": [
            "Nilai 'a' harus koprima dengan 26 (pilihan: 1,3,5,7,9,11,15,17,19,21,23,25)",
            "Nilai a = {a}",
            "Nilai b = {b}"
        ]
    },
    # Hard challenges
    "vigenere_hard_1": {
        "id": "vigenere_hard_1",
        "title": "Kriptoanalisis Vigenère Lanjutan",
        "description": "Pecahkan ciphertext Vigenère berikut. Kunci lebih panjang dan teks lebih pendek.",
        "difficulty": "sulit",
        "points": 500,
        "type": "pecahkan_sandi",
        "cipher": "vigenere",
        "hints": [
            "Index of Coincidence dapat membantu menemukan panjang kunci",
            "Panjang kunci = {key_len}",
            "Kunci = '{key}'"
        ]
    },
    "mixed_hard_1": {
        "id": "mixed_hard_1",
        "title": "Identifikasi & Pecahkan",
        "description": "Ciphertext ini dienkripsi dengan salah satu sandi klasik. Identifikasi jenisnya lalu pecahkan!",
        "difficulty": "sulit",
        "points": 500,
        "type": "pecahkan_sandi",
        "cipher": "random",
        "hints": [
            "Analisis distribusi huruf untuk mengidentifikasi jenis sandi",
            "Ini adalah {cipher_name}",
            "Kunci: {key}"
        ]
    }
}

SAMPLE_PLAINTEXTS = [
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
    "CRYPTOGRAPHY IS THE PRACTICE OF SECURE COMMUNICATION",
    "INFORMATION SECURITY IS VERY IMPORTANT IN MODERN WORLD",
    "ATTACK AT DAWN AND CAPTURE THE FLAG",
    "KNOWLEDGE IS POWER AND SECURITY IS ESSENTIAL",
    "MATHEMATICS IS THE QUEEN OF ALL SCIENCES",
    "SECRET MESSAGES MUST BE PROTECTED AT ALL COSTS",
    "ENCRYPTION TRANSFORMS READABLE DATA INTO SCRAMBLED TEXT",
    "ALICE SENDS A MESSAGE TO BOB USING ENCRYPTION",
    "THE ART OF WAR IS THE ART OF DECEPTION",
]

VIGENERE_KEYS_SHORT = ["KEY", "SUN", "CAT", "DOG", "RAT", "OWL", "BIG", "RED"]
VIGENERE_KEYS_LONG = ["SECRET", "CIPHER", "CASTLE", "DRAGON", "KNIGHT", "SHIELD"]


def generate_challenge(challenge_id: str | None = None) -> tuple[dict, str]:
    """Generate a specific or random challenge instance."""
    if challenge_id and challenge_id in CHALLENGES:
        template = CHALLENGES[challenge_id]
    else:
        template = random.choice(list(CHALLENGES.values()))

    challenge = dict(template)
    plaintext = random.choice(SAMPLE_PLAINTEXTS)

    if challenge["cipher"] == "caesar":
        shift = random.randint(1, 25)
        result = caesar_encrypt(plaintext, shift)
        challenge["ciphertext"] = result["output"]
        challenge["answer"] = plaintext
        challenge["_key"] = shift
        challenge["hints"] = [h.format(shift=shift) for h in challenge["hints"]]
        if "{plain_hint}" in challenge.get("description", ""):
            challenge["description"] = challenge["description"].format(
                plain_hint=plaintext[:5]
            )

    elif challenge["cipher"] == "vigenere":
        if challenge["difficulty"] == "sulit":
            key = random.choice(VIGENERE_KEYS_LONG)
        else:
            key = random.choice(VIGENERE_KEYS_SHORT)
        result = vigenere_encrypt(plaintext, key)
        challenge["ciphertext"] = result["output"]
        challenge["answer"] = plaintext
        challenge["_key"] = key
        challenge["hints"] = [
            h.format(key=key, key_len=len(key), key_start=key[:2])
            for h in challenge["hints"]
        ]

    elif challenge["cipher"] == "affine":
        a_options = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        a = random.choice(a_options)
        b = random.randint(1, 25)
        result = affine_encrypt(plaintext, a, b)
        challenge["ciphertext"] = result["output"]
        challenge["answer"] = plaintext
        challenge["_key"] = {"a": a, "b": b}
        challenge["hints"] = [h.format(a=a, b=b) for h in challenge["hints"]]

    elif challenge["cipher"] == "random":
        cipher_type = random.choice(["caesar", "vigenere", "affine"])
        if cipher_type == "caesar":
            shift = random.randint(1, 25)
            result = caesar_encrypt(plaintext, shift)
            challenge["ciphertext"] = result["output"]
            challenge["answer"] = plaintext
            challenge["_key"] = shift
            cipher_name = "Caesar Cipher"
            key_str = f"shift={shift}"
        elif cipher_type == "vigenere":
            key = random.choice(VIGENERE_KEYS_SHORT)
            result = vigenere_encrypt(plaintext, key)
            challenge["ciphertext"] = result["output"]
            challenge["answer"] = plaintext
            challenge["_key"] = key
            cipher_name = "Vigenère Cipher"
            key_str = key
        else:
            a_options = [3, 5, 7, 9, 11]
            a = random.choice(a_options)
            b = random.randint(1, 10)
            result = affine_encrypt(plaintext, a, b)
            challenge["ciphertext"] = result["output"]
            challenge["answer"] = plaintext
            challenge["_key"] = {"a": a, "b": b}
            cipher_name = "Affine Cipher"
            key_str = f"a={a}, b={b}"
        challenge["hints"] = [
            h.format(cipher_name=cipher_name, key=key_str)
            for h in challenge["hints"]
        ]

    # Generate unique token for this instance
    token = hashlib.md5(f"{challenge['id']}:{challenge.get('ciphertext','')}:{time.time()}".encode()).hexdigest()[:12]
    challenge["token"] = token

    # Remove internal answer from response
    safe_challenge = {k: v for k, v in challenge.items() if k != "answer" and k != "_key"}
    safe_challenge["_answer_hash"] = hashlib.sha256(plaintext.encode()).hexdigest()

    return safe_challenge, plaintext


def check_answer(user_answer: str, correct_answer: str) -> dict:
    """Check if user's answer matches."""
    user_clean = user_answer.strip().upper().replace("  ", " ")
    correct_clean = correct_answer.strip().upper()

    exact_match = user_clean == correct_clean
    partial = correct_clean.startswith(user_clean) or user_clean.startswith(correct_clean)
    similarity = _similarity(user_clean, correct_clean)

    return {
        "correct": exact_match,
        "partial_match": partial and not exact_match,
        "similarity": round(similarity * 100, 1),
        "feedback": "Benar! 🎉" if exact_match else
                   "Hampir benar! Periksa kembali." if similarity > 0.8 else
                   "Belum tepat. Coba lagi!"
    }


def _similarity(a: str, b: str) -> float:
    """Simple character-based similarity."""
    if not a or not b:
        return 0.0
    matches = sum(1 for x, y in zip(a, b) if x == y)
    return matches / max(len(a), len(b))


def get_leaderboard(limit: int = 20) -> list:
    """Get top scores from database."""
    from app.models import ChallengeScore
    scores = ChallengeScore.query.filter_by(solved=True)\
        .order_by(ChallengeScore.score.desc())\
        .limit(limit).all()
    return [{
        "username": s.username,
        "challenge_id": s.challenge_id,
        "difficulty": s.difficulty,
        "score": s.score,
        "hints_used": s.hints_used,
        "time_seconds": s.time_seconds,
        "date": s.created_at.strftime("%Y-%m-%d %H:%M")
    } for s in scores]
