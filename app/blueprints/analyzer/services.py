"""
Analyzer Service — cipher detection, entropy analysis, frequency analysis.
"""
import math
import string
from collections import Counter


ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}


def shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not text:
        return 0.0
    counter = Counter(text)
    length = len(text)
    entropy = 0.0
    for count in counter.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return round(entropy, 4)


def index_of_coincidence(text: str) -> float:
    """Calculate Index of Coincidence for alphabetic characters."""
    upper = text.upper()
    letters = [c for c in upper if c.isalpha()]
    n = len(letters)
    if n <= 1:
        return 0.0
    counter = Counter(letters)
    ic = sum(f * (f - 1) for f in counter.values()) / (n * (n - 1))
    return round(ic, 6)


def chi_squared(text: str) -> float:
    """Chi-squared statistic vs English letter frequency."""
    upper = text.upper()
    letters = [c for c in upper if c.isalpha()]
    n = len(letters)
    if n == 0:
        return 999.0
    counter = Counter(letters)
    chi_sq = 0.0
    for letter in string.ascii_uppercase:
        observed = counter.get(letter, 0) / n * 100
        expected = ENGLISH_FREQ.get(letter, 0)
        if expected > 0:
            chi_sq += (observed - expected) ** 2 / expected
    return round(chi_sq, 2)


def letter_distribution(text: str) -> dict:
    """Get letter frequency distribution."""
    upper = text.upper()
    letters = [c for c in upper if c.isalpha()]
    total = len(letters)
    if total == 0:
        return {"labels": list(string.ascii_uppercase), "counts": [0]*26, "percentages": [0.0]*26}
    counter = Counter(letters)
    counts = [counter.get(l, 0) for l in string.ascii_uppercase]
    percentages = [round(c / total * 100, 2) for c in counts]
    return {
        "labels": list(string.ascii_uppercase),
        "counts": counts,
        "percentages": percentages,
        "total": total
    }


def detect_cipher(text: str) -> dict:
    """Attempt to detect the cipher type used on a ciphertext."""
    if not text or len(text.strip()) < 3:
        return {"error": "Teks terlalu pendek untuk analisis."}

    upper = text.upper()
    letters_only = [c for c in upper if c.isalpha()]
    total_chars = len(text)
    total_letters = len(letters_only)
    has_numbers = any(c.isdigit() for c in text)
    has_spaces = ' ' in text
    all_hex = all(c in '0123456789abcdefABCDEF ' for c in text.strip())
    all_numeric = all(c.isdigit() or c == ' ' for c in text.strip())

    entropy = shannon_entropy(text)
    ic = index_of_coincidence(text) if total_letters > 1 else 0
    chi = chi_squared(text) if total_letters > 0 else 999
    dist = letter_distribution(text)

    candidates = []

    # Check for hash (hex string of specific length)
    stripped = text.strip()
    if all_hex and not has_spaces and len(stripped) in [32, 40, 64, 128]:
        candidates.append({
            "cipher": "Hash (MD5/SHA-1/SHA-256/SHA-512)",
            "confidence": 95,
            "reason": f"String heksadesimal dengan panjang {len(stripped)} karakter"
        })

    # Check for RSA / numeric cipher
    if all_numeric and has_spaces:
        numbers = stripped.split()
        if all(len(n) > 2 for n in numbers):
            candidates.append({
                "cipher": "RSA / Enkripsi Numerik",
                "confidence": 80,
                "reason": "Deretan angka besar dipisah spasi"
            })

    # Check for Base64
    import re
    if re.match(r'^[A-Za-z0-9+/]+=*$', stripped) and len(stripped) > 10:
        if len(stripped) % 4 == 0:
            candidates.append({
                "cipher": "Base64 Encoding",
                "confidence": 70,
                "reason": "Karakter Base64 valid dengan padding"
            })

    # Letter-based analysis
    if total_letters > 0:
        # IC close to English (~0.0667) suggests monoalphabetic
        if 0.060 <= ic <= 0.075:
            candidates.append({
                "cipher": "Caesar / Sandi Substitusi Monoalfabetik",
                "confidence": min(85, int(70 + (1 - abs(ic - 0.0667) / 0.01) * 15)),
                "reason": f"IC={ic:.4f} mendekati IC bahasa Inggris (0.0667)"
            })
            if chi < 50:
                candidates[-1]["confidence"] = min(95, candidates[-1]["confidence"] + 10)
                candidates[-1]["reason"] += f", χ²={chi} rendah"
            # If all uppercase no spaces, likely Affine or simple substitution
            if text == text.upper() and not has_spaces:
                candidates.append({
                    "cipher": "Affine Cipher",
                    "confidence": 55,
                    "reason": "Teks huruf besar tanpa spasi, IC monoalfabetik"
                })

        # IC between 0.038-0.060 suggests polyalphabetic
        if 0.035 <= ic < 0.060:
            candidates.append({
                "cipher": "Vigenère / Sandi Polialfabetik",
                "confidence": min(80, int(60 + (0.060 - ic) / 0.025 * 20)),
                "reason": f"IC={ic:.4f} di antara acak dan Inggris"
            })

        # IC near 0.038 (random) with alphabetic text
        if ic < 0.042 and total_letters > 20:
            candidates.append({
                "cipher": "Sandi Polialfabetik Kuat / Teks Acak",
                "confidence": 60,
                "reason": f"IC={ic:.4f} mendekati acak (0.0385)"
            })

        # Check for Playfair clues
        if text == text.upper() and len(letters_only) % 2 == 0:
            has_j = 'J' in upper
            double_pairs = any(letters_only[i] == letters_only[i+1]
                             for i in range(0, len(letters_only)-1, 2))
            if not has_j and not double_pairs:
                candidates.append({
                    "cipher": "Playfair Cipher",
                    "confidence": 50,
                    "reason": "Panjang genap, tanpa J, tanpa pasangan huruf kembar"
                })

        # Hill cipher clue
        if text == text.upper() and not has_spaces and len(letters_only) % 3 == 0:
            candidates.append({
                "cipher": "Hill Cipher",
                "confidence": 40,
                "reason": "Teks huruf besar, panjang kelipatan 3"
            })

    # High entropy suggests modern encryption
    if entropy > 4.5 and not all_hex:
        candidates.append({
            "cipher": "Enkripsi Modern (AES/DES/dll)",
            "confidence": 65,
            "reason": f"Entropi tinggi ({entropy} bit)"
        })

    # Sort by confidence
    candidates.sort(key=lambda x: x["confidence"], reverse=True)

    if not candidates:
        candidates.append({
            "cipher": "Tidak Terdeteksi",
            "confidence": 0,
            "reason": "Tidak dapat mengidentifikasi pola sandi"
        })

    return {
        "input": text[:200] + ("..." if len(text) > 200 else ""),
        "analysis": {
            "total_chars": total_chars,
            "total_letters": total_letters,
            "entropy": entropy,
            "index_of_coincidence": ic,
            "chi_squared": chi,
            "has_numbers": has_numbers,
            "has_spaces": has_spaces,
            "all_hex": all_hex
        },
        "candidates": candidates[:5],
        "distribution": dist
    }


def entropy_analysis(text: str, encrypted_text: str = None) -> dict:
    """Full entropy analysis with optional comparison."""
    if not text:
        return {"error": "Teks diperlukan."}

    entropy = shannon_entropy(text)
    dist = letter_distribution(text)
    char_dist = Counter(text)
    total_chars = len(text)
    unique_chars = len(char_dist)

    # Randomness score (0-100): higher = more random
    max_entropy = math.log2(unique_chars) if unique_chars > 1 else 1
    randomness = round((entropy / max_entropy) * 100, 1) if max_entropy > 0 else 0

    result = {
        "text_preview": text[:100] + ("..." if len(text) > 100 else ""),
        "entropy": entropy,
        "max_possible_entropy": round(max_entropy, 4),
        "randomness_score": randomness,
        "total_chars": total_chars,
        "unique_chars": unique_chars,
        "letter_distribution": dist,
        "char_distribution": {
            "labels": [repr(k) if not k.isalnum() else k for k in sorted(char_dist.keys())],
            "counts": [char_dist[k] for k in sorted(char_dist.keys())]
        }
    }

    if encrypted_text:
        enc_entropy = shannon_entropy(encrypted_text)
        enc_dist = letter_distribution(encrypted_text)
        enc_char_dist = Counter(encrypted_text)
        enc_unique = len(enc_char_dist)
        enc_max = math.log2(enc_unique) if enc_unique > 1 else 1
        enc_randomness = round((enc_entropy / enc_max) * 100, 1) if enc_max > 0 else 0

        result["comparison"] = {
            "plaintext": {
                "entropy": entropy,
                "randomness_score": randomness,
                "unique_chars": unique_chars
            },
            "encrypted": {
                "entropy": enc_entropy,
                "randomness_score": enc_randomness,
                "unique_chars": enc_unique,
                "letter_distribution": enc_dist
            },
            "entropy_increase": round(enc_entropy - entropy, 4),
            "randomness_increase": round(enc_randomness - randomness, 1)
        }

    return result
