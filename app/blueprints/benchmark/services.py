"""
Benchmark Service — performance comparison of cryptographic algorithms.
"""
import time
import string
import random


def _generate_text(length: int) -> str:
    """Generate random plaintext for benchmarking."""
    return ''.join(random.choices(string.ascii_uppercase + ' ', k=length))


def run_benchmark(text_sizes: list = None, iterations: int = 10) -> dict:
    """Run benchmark comparison across all algorithms."""
    if text_sizes is None:
        text_sizes = [100, 500, 1000, 5000]

    iterations = max(1, min(iterations, 50))

    results = {}
    algorithms = {
        "Caesar": _bench_caesar,
        "Vigenère": _bench_vigenere,
        "Affine": _bench_affine,
        "AES-128": _bench_aes,
        "RSA": _bench_rsa,
        "SHA-256": _bench_sha256,
    }

    for algo_name, bench_fn in algorithms.items():
        results[algo_name] = {
            "timings": [],
            "sizes": text_sizes,
        }
        for size in text_sizes:
            text = _generate_text(size)
            times = []
            for _ in range(iterations):
                try:
                    elapsed = bench_fn(text)
                    times.append(elapsed)
                except Exception:
                    times.append(-1)
            avg = sum(t for t in times if t >= 0) / max(1, len([t for t in times if t >= 0]))
            results[algo_name]["timings"].append({
                "size": size,
                "avg_ms": round(avg * 1000, 3),
                "min_ms": round(min(t for t in times if t >= 0) * 1000, 3) if any(t >= 0 for t in times) else -1,
                "max_ms": round(max(t for t in times if t >= 0) * 1000, 3) if any(t >= 0 for t in times) else -1,
                "iterations": iterations
            })

    # Build chart data
    chart_data = {
        "labels": [str(s) for s in text_sizes],
        "datasets": []
    }
    colors = {
        "Caesar": "#EF4444",
        "Vigenère": "#F59E0B",
        "Affine": "#10B981",
        "AES-128": "#6366F1",
        "RSA": "#EC4899",
        "SHA-256": "#8B5CF6"
    }
    for algo_name, data in results.items():
        chart_data["datasets"].append({
            "label": algo_name,
            "data": [t["avg_ms"] for t in data["timings"]],
            "borderColor": colors.get(algo_name, "#94A3B8"),
            "backgroundColor": colors.get(algo_name, "#94A3B8") + "20",
            "fill": False,
            "tension": 0.3
        })

    # Complexity info
    complexity = {
        "Caesar": {"time": "O(n)", "space": "O(n)", "type": "Substitusi"},
        "Vigenère": {"time": "O(n)", "space": "O(n)", "type": "Substitusi Polialfabetik"},
        "Affine": {"time": "O(n)", "space": "O(n)", "type": "Substitusi"},
        "AES-128": {"time": "O(n)", "space": "O(1)", "type": "Block Cipher"},
        "RSA": {"time": "O(n · k²)", "space": "O(n)", "type": "Asimetris"},
        "SHA-256": {"time": "O(n)", "space": "O(1)", "type": "Hash"}
    }

    return {
        "results": results,
        "chart_data": chart_data,
        "complexity": complexity,
        "config": {
            "text_sizes": text_sizes,
            "iterations": iterations
        }
    }


def _bench_caesar(text: str) -> float:
    from app.blueprints.classical.services import caesar_encrypt
    start = time.perf_counter()
    caesar_encrypt(text, 13)
    return time.perf_counter() - start


def _bench_vigenere(text: str) -> float:
    from app.blueprints.classical.services import vigenere_encrypt
    start = time.perf_counter()
    vigenere_encrypt(text, "SECRETKEY")
    return time.perf_counter() - start


def _bench_affine(text: str) -> float:
    from app.blueprints.classical.services import affine_encrypt
    start = time.perf_counter()
    affine_encrypt(text, 5, 8)
    return time.perf_counter() - start


def _bench_aes(text: str) -> float:
    from app.blueprints.modern.services import aes_encrypt_demo
    start = time.perf_counter()
    aes_encrypt_demo(text[:16], "BenchmarkKey1234")
    return time.perf_counter() - start


def _bench_rsa(text: str) -> float:
    from app.blueprints.modern.services import rsa_encrypt
    start = time.perf_counter()
    # RSA encrypts char-by-char, limit to first 10 chars for fairness
    rsa_encrypt(text[:10], 65537, 2773)
    return time.perf_counter() - start


def _bench_sha256(text: str) -> float:
    import hashlib
    start = time.perf_counter()
    hashlib.sha256(text.encode()).hexdigest()
    return time.perf_counter() - start
