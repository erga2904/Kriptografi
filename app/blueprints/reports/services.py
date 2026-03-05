"""
Report Service — generate experiment reports in PDF and TXT.
"""
import io
import time
from datetime import datetime


def generate_txt_report(data: dict) -> str:
    """Generate plain text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("    LAPORAN EKSPERIMEN KRIPTOGRAFI — CipherLab")
    lines.append("=" * 60)
    lines.append(f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append(f"Algoritma  : {data.get('algorithm', 'N/A')}")
    lines.append(f"Operasi    : {data.get('operation', 'N/A')}")
    lines.append(f"Kunci      : {data.get('key', 'N/A')}")
    lines.append("")

    lines.append("─" * 60)
    lines.append("INPUT (Plaintext):")
    lines.append(data.get("plaintext", "N/A"))
    lines.append("")

    lines.append("─" * 60)
    lines.append("OUTPUT (Ciphertext):")
    lines.append(data.get("ciphertext", "N/A"))
    lines.append("")

    if data.get("execution_time"):
        lines.append("─" * 60)
        lines.append(f"Waktu Eksekusi: {data['execution_time']} ms")

    if data.get("steps"):
        lines.append("")
        lines.append("─" * 60)
        lines.append("LANGKAH-LANGKAH PROSES:")
        for i, step in enumerate(data["steps"][:20], 1):
            if isinstance(step, dict):
                step_str = " | ".join(f"{k}: {v}" for k, v in step.items())
            else:
                step_str = str(step)
            lines.append(f"  {i}. {step_str}")

    if data.get("analysis"):
        lines.append("")
        lines.append("─" * 60)
        lines.append("ANALISIS:")
        for k, v in data["analysis"].items():
            lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("Dibuat oleh CipherLab — Platform Pembelajaran Kriptografi")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_pdf_report(data: dict) -> bytes:
    """Generate PDF report."""
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Laporan Eksperimen Kriptografi", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, "CipherLab - Platform Pembelajaran Kriptografi", ln=True, align="C")
    pdf.cell(0, 6, f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(8)

    # Algorithm Info
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Informasi Algoritma", ln=True)
    pdf.set_draw_color(99, 102, 241)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    info = [
        ("Algoritma", data.get("algorithm", "N/A")),
        ("Operasi", data.get("operation", "N/A")),
        ("Kunci", str(data.get("key", "N/A"))),
    ]
    if data.get("execution_time"):
        info.append(("Waktu Eksekusi", f"{data['execution_time']} ms"))

    for label, value in info:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 7, f"{label}:")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, str(value)[:80], ln=True)
    pdf.ln(4)

    # Input
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Input (Plaintext)", ln=True)
    pdf.set_draw_color(99, 102, 241)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Courier", "", 9)
    plaintext = data.get("plaintext", "N/A")
    pdf.multi_cell(0, 5, plaintext[:500])
    pdf.ln(4)

    # Output
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Output (Ciphertext)", ln=True)
    pdf.set_draw_color(99, 102, 241)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Courier", "", 9)
    ciphertext = data.get("ciphertext", "N/A")
    pdf.multi_cell(0, 5, str(ciphertext)[:500])
    pdf.ln(4)

    # Steps
    if data.get("steps"):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Langkah-langkah Proses", ln=True)
        pdf.set_draw_color(99, 102, 241)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        pdf.set_font("Courier", "", 8)
        for i, step in enumerate(data["steps"][:15], 1):
            if isinstance(step, dict):
                step_str = " | ".join(f"{k}: {v}" for k, v in step.items())
            else:
                step_str = str(step)
            text = f"{i}. {step_str}"
            pdf.multi_cell(0, 4, text[:120])
        pdf.ln(4)

    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 8, "Dibuat oleh CipherLab - Platform Pembelajaran Kriptografi", ln=True, align="C")

    return pdf.output()
