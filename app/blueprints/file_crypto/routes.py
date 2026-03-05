"""
File Encryption API Routes — encrypt/decrypt uploaded files.
"""
import os
import io
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app.blueprints.file_crypto.services import encrypt_file_data, decrypt_file_data

file_crypto_bp = Blueprint("file_crypto", __name__)

ALLOWED_EXTENSIONS = {
    "txt", "pdf", "doc", "docx", "csv", "json", "xml",
    "png", "jpg", "jpeg", "gif", "bmp",
    "zip", "gz", "tar",
    "py", "js", "html", "css", "md",
    "enc",  # encrypted files
}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@file_crypto_bp.route("/encrypt", methods=["POST"])
def encrypt():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400

    file = request.files["file"]
    password = request.form.get("password", "")

    if not file.filename:
        return jsonify({"error": "Nama file kosong"}), 400
    if not password:
        return jsonify({"error": "Password diperlukan"}), 400
    if not _allowed(file.filename):
        return jsonify({"error": "Tipe file tidak diizinkan"}), 400

    file_data = file.read()
    if len(file_data) > 16 * 1024 * 1024:
        return jsonify({"error": "Ukuran file melebihi batas 16 MB"}), 400

    try:
        encrypted = encrypt_file_data(file_data, password)
        buf = io.BytesIO(encrypted)
        buf.seek(0)

        safe_name = secure_filename(file.filename) + ".enc"
        return send_file(
            buf,
            as_attachment=True,
            download_name=safe_name,
            mimetype="application/octet-stream",
        )
    except Exception as e:
        return jsonify({"error": f"Gagal mengenkripsi: {str(e)}"}), 500


@file_crypto_bp.route("/decrypt", methods=["POST"])
def decrypt():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400

    file = request.files["file"]
    password = request.form.get("password", "")

    if not file.filename:
        return jsonify({"error": "Nama file kosong"}), 400
    if not password:
        return jsonify({"error": "Password diperlukan"}), 400

    file_data = file.read()

    try:
        decrypted = decrypt_file_data(file_data, password)
        buf = io.BytesIO(decrypted)
        buf.seek(0)

        # Remove .enc extension if present
        original_name = file.filename
        if original_name.endswith(".enc"):
            original_name = original_name[:-4]
        safe_name = secure_filename(original_name) if original_name else "decrypted_file"

        return send_file(
            buf,
            as_attachment=True,
            download_name=safe_name,
            mimetype="application/octet-stream",
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Gagal mendekripsi: {str(e)}"}), 500


@file_crypto_bp.route("/info", methods=["POST"])
def file_info():
    """Get info about an encrypted file without decrypting."""
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400

    file = request.files["file"]
    file_data = file.read()

    is_encrypted = file_data[:7] == b"CPHRLAB"
    size = len(file_data)

    return jsonify({
        "filename": file.filename,
        "size": size,
        "size_readable": f"{size / 1024:.1f} KB" if size < 1048576 else f"{size / 1048576:.1f} MB",
        "is_cipherlab_encrypted": is_encrypted,
        "format": "CipherLab AES-256-CBC" if is_encrypted else "Tidak terenkripsi / format lain",
    })
