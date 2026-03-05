"""
Report Generator API Routes — generate TXT and PDF reports.
"""
import io
from flask import Blueprint, request, jsonify, send_file
from app.blueprints.reports.services import generate_txt_report, generate_pdf_report

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/generate-txt", methods=["POST"])
def gen_txt():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return jsonify({"error": "Data laporan diperlukan"}), 400

    txt = generate_txt_report(data)
    buf = io.BytesIO(txt.encode("utf-8"))
    buf.seek(0)

    return send_file(
        buf,
        as_attachment=True,
        download_name="cipherlab_report.txt",
        mimetype="text/plain",
    )


@reports_bp.route("/generate-pdf", methods=["POST"])
def gen_pdf():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return jsonify({"error": "Data laporan diperlukan"}), 400

    try:
        pdf_bytes = generate_pdf_report(data)
        buf = io.BytesIO(pdf_bytes)
        buf.seek(0)

        return send_file(
            buf,
            as_attachment=True,
            download_name="cipherlab_report.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        return jsonify({"error": f"Gagal membuat PDF: {str(e)}"}), 500
