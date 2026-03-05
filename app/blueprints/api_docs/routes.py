"""
API Docs Blueprint — serves the documentation page.
"""
from flask import Blueprint

api_docs_bp = Blueprint("api_docs", __name__)

# This blueprint doesn't need API routes.
# The /api-docs page is served by the main blueprint.
# But we provide an endpoint listing for the docs page.


@api_docs_bp.route("/endpoints", methods=["GET"])
def endpoints():
    from flask import jsonify
    docs = {
        "version": "2.0",
        "base_url": "/api",
        "endpoints": [
            {
                "group": "Playground",
                "routes": [
                    {"method": "POST", "path": "/playground/run", "desc": "Jalankan algoritma kriptografi", "params": ["algorithm", "mode", "text", "params"]},
                    {"method": "GET",  "path": "/playground/algorithms", "desc": "Daftar algoritma tersedia"},
                ]
            },
            {
                "group": "Analyzer",
                "routes": [
                    {"method": "POST", "path": "/analyzer/detect", "desc": "Deteksi jenis cipher dari teks", "params": ["text"]},
                    {"method": "POST", "path": "/analyzer/entropy", "desc": "Analisis entropi teks", "params": ["text", "encrypted_text (opsional)"]},
                ]
            },
            {
                "group": "Simulator",
                "routes": [
                    {"method": "POST", "path": "/simulator/rsa-visual", "desc": "Simulasi visual RSA key generation", "params": ["p", "q", "bits"]},
                ]
            },
            {
                "group": "Tantangan",
                "routes": [
                    {"method": "GET", "path": "/challenges/list", "desc": "Daftar tantangan tersedia"},
                    {"method": "POST", "path": "/challenges/generate", "desc": "Generate tantangan baru", "params": ["challenge_id"]},
                    {"method": "POST", "path": "/challenges/check", "desc": "Periksa jawaban", "params": ["answer", "correct_answer", "challenge_id"]},
                    {"method": "GET",  "path": "/challenges/leaderboard", "desc": "Papan peringkat", "params": ["limit"]},
                ]
            },
            {
                "group": "Enkripsi File",
                "routes": [
                    {"method": "POST", "path": "/file-crypto/encrypt", "desc": "Enkripsi file (multipart)", "params": ["file", "password"]},
                    {"method": "POST", "path": "/file-crypto/decrypt", "desc": "Dekripsi file (multipart)", "params": ["file", "password"]},
                    {"method": "POST", "path": "/file-crypto/info", "desc": "Info file terenkripsi", "params": ["file"]},
                ]
            },
            {
                "group": "Key Generator",
                "routes": [
                    {"method": "POST", "path": "/keygen/rsa", "desc": "Generate RSA keypair", "params": ["bits"]},
                    {"method": "POST", "path": "/keygen/aes", "desc": "Generate AES key", "params": ["bits"]},
                    {"method": "POST", "path": "/keygen/random", "desc": "Generate random key", "params": ["length", "charset"]},
                    {"method": "POST", "path": "/keygen/hmac", "desc": "Generate HMAC key", "params": ["bits"]},
                ]
            },
            {
                "group": "Benchmark",
                "routes": [
                    {"method": "POST", "path": "/benchmark/run", "desc": "Jalankan benchmark performa", "params": ["text_sizes", "iterations"]},
                ]
            },
            {
                "group": "Laporan",
                "routes": [
                    {"method": "POST", "path": "/reports/generate-txt", "desc": "Generate laporan TXT"},
                    {"method": "POST", "path": "/reports/generate-pdf", "desc": "Generate laporan PDF"},
                ]
            },
            {
                "group": "Code Generator",
                "routes": [
                    {"method": "GET",  "path": "/codegen/algorithms", "desc": "Daftar algoritma untuk code generation"},
                    {"method": "POST", "path": "/codegen/generate", "desc": "Generate kode implementasi", "params": ["algorithm", "language"]},
                ]
            },
            {
                "group": "Klasik",
                "routes": [
                    {"method": "POST", "path": "/classical/caesar", "desc": "Caesar cipher"},
                    {"method": "POST", "path": "/classical/vigenere", "desc": "Vigenère cipher"},
                    {"method": "POST", "path": "/classical/affine", "desc": "Affine cipher"},
                    {"method": "POST", "path": "/classical/playfair", "desc": "Playfair cipher"},
                    {"method": "POST", "path": "/classical/hill", "desc": "Hill cipher"},
                ]
            },
            {
                "group": "Modern",
                "routes": [
                    {"method": "POST", "path": "/modern/aes", "desc": "AES encryption"},
                    {"method": "POST", "path": "/modern/rsa", "desc": "RSA encryption"},
                    {"method": "POST", "path": "/modern/sha256", "desc": "SHA-256 hashing"},
                    {"method": "POST", "path": "/modern/rsa-keygen", "desc": "RSA key generation"},
                ]
            },
        ]
    }
    return jsonify(docs)
