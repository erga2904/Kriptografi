"""
Attack Simulation Services
Brute force, frequency analysis, RSA weak key attacks.
"""
import math
import string
from collections import Counter


# Standard English letter frequencies
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}


def brute_force_caesar(ciphertext: str) -> dict:
    """Try all 26 shifts and rank by English frequency score."""
    results = []
    for shift in range(26):
        decrypted = []
        for ch in ciphertext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                decrypted.append(chr((ord(ch) - base - shift) % 26 + base))
            else:
                decrypted.append(ch)
        text = "".join(decrypted)

        # Score by frequency similarity
        upper = text.upper()
        total = sum(1 for c in upper if c.isalpha())
        if total == 0:
            score = 0
        else:
            score = 0
            for letter in string.ascii_uppercase:
                observed = upper.count(letter) / total * 100
                expected = ENGLISH_FREQ.get(letter, 0)
                score -= (observed - expected) ** 2  # Higher is better (less deviation)

        results.append({
            "shift": shift,
            "decrypted": text,
            "score": round(score, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {
        "input": ciphertext,
        "best_guess": results[0],
        "all_results": results,
        "method": "Brute force: try all 26 shifts, rank by English letter frequency χ²"
    }


def frequency_analysis(text: str) -> dict:
    """Analyze letter frequency distribution."""
    upper = text.upper()
    letters_only = [c for c in upper if c.isalpha()]
    total = len(letters_only)

    if total == 0:
        return {"error": "No alphabetic characters in input."}

    counter = Counter(letters_only)
    frequencies = {}
    for letter in string.ascii_uppercase:
        count = counter.get(letter, 0)
        frequencies[letter] = {
            "count": count,
            "percentage": round(count / total * 100, 2),
            "expected": ENGLISH_FREQ[letter]
        }

    # Sort by frequency
    sorted_by_freq = sorted(frequencies.items(), key=lambda x: x[1]["count"], reverse=True)

    # Chi-squared test
    chi_sq = 0
    for letter in string.ascii_uppercase:
        observed = counter.get(letter, 0) / total * 100
        expected = ENGLISH_FREQ[letter]
        if expected > 0:
            chi_sq += (observed - expected) ** 2 / expected

    # IC (Index of Coincidence)
    ic = sum(counter[l] * (counter[l] - 1) for l in counter) / (total * (total - 1)) if total > 1 else 0

    return {
        "input": text,
        "total_letters": total,
        "frequencies": frequencies,
        "sorted_frequencies": [{"letter": k, **v} for k, v in sorted_by_freq],
        "chi_squared": round(chi_sq, 2),
        "index_of_coincidence": round(ic, 4),
        "expected_english_ic": 0.0667,
        "chart_data": {
            "labels": list(string.ascii_uppercase),
            "observed": [frequencies[l]["percentage"] for l in string.ascii_uppercase],
            "expected": [ENGLISH_FREQ[l] for l in string.ascii_uppercase]
        },
        "math": "IC = Σ f_i(f_i - 1) / N(N-1), English IC ≈ 0.0667"
    }


def rsa_weak_key_attack(n: int, e: int = 65537) -> dict:
    """Attempt to factor n using trial division and Fermat's method."""
    steps = []

    # Trial division
    steps.append({"method": "Trial Division", "status": "starting"})
    factor = None
    trial_steps = []
    for i in range(2, min(100000, int(math.isqrt(n)) + 1)):
        if n % i == 0:
            factor = i
            trial_steps.append({
                "divisor": i,
                "result": f"{n} ÷ {i} = {n // i}",
                "found": True
            })
            break
        if i <= 100 or i % 1000 == 0:
            trial_steps.append({
                "divisor": i,
                "result": f"{n} mod {i} = {n % i}",
                "found": False
            })

    if factor:
        p, q = factor, n // factor
        phi_n = (p - 1) * (q - 1)
        g, x, _ = _ext_gcd(e % phi_n, phi_n)
        d = x % phi_n if g == 1 else None

        steps.append({
            "method": "Trial Division",
            "status": "SUCCESS",
            "p": p, "q": q,
            "phi_n": phi_n,
            "d": d,
            "attempts": len(trial_steps),
            "trial_log": trial_steps[:20]  # Limit log size
        })

        return {
            "n": n, "e": e,
            "attack_successful": True,
            "p": p, "q": q,
            "phi_n": phi_n,
            "private_key_d": d,
            "method": "Trial Division",
            "steps": steps,
            "math": f"n = {p} × {q}, φ(n) = {phi_n}, d = {d}"
        }

    # Fermat's factorization
    steps.append({"method": "Fermat's Factorization", "status": "starting"})
    a = math.isqrt(n) + 1
    fermat_steps = []
    fermat_found = False

    for attempt in range(10000):
        b_sq = a * a - n
        b = math.isqrt(b_sq)
        fermat_steps.append({
            "a": a,
            "a²-n": b_sq,
            "b": b,
            "is_perfect_square": b * b == b_sq
        })
        if b * b == b_sq:
            p, q = a + b, a - b
            if p > 1 and q > 1:
                fermat_found = True
                phi_n = (p - 1) * (q - 1)
                g, x, _ = _ext_gcd(e % phi_n, phi_n)
                d = x % phi_n if g == 1 else None
                steps.append({
                    "method": "Fermat's Factorization",
                    "status": "SUCCESS",
                    "p": p, "q": q,
                    "phi_n": phi_n,
                    "d": d,
                    "attempts": attempt + 1,
                    "fermat_log": fermat_steps[:20]
                })
                return {
                    "n": n, "e": e,
                    "attack_successful": True,
                    "p": p, "q": q,
                    "phi_n": phi_n,
                    "private_key_d": d,
                    "method": "Fermat's Factorization",
                    "steps": steps,
                    "math": f"n = {p} × {q}, φ(n) = {phi_n}, d = {d}"
                }
        a += 1

    steps.append({
        "method": "Fermat's Factorization",
        "status": "FAILED",
        "fermat_log": fermat_steps[:20]
    })

    return {
        "n": n, "e": e,
        "attack_successful": False,
        "message": "Could not factor n within limits. Key appears reasonably strong.",
        "steps": steps
    }


def _ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = _ext_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1
