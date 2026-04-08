"""
Main Blueprint — serves all HTML pages (SPA-like navigation).
CipherLab v2.0
"""
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


# ── Core Pages ───────────────────────────────────────────────────
from jinja2 import TemplateNotFound
@main_bp.route("/")
def index():
    return render_template("index.html")
    try:
        return render_template("encryption_table.html")
    except TemplateNotFound:
        # Keep endpoint alive if deployment bundle misses the new template.
        return render_template("index.html")

@main_bp.route("/classical")
def classical():
    return render_template("classical.html")


@main_bp.route("/modern")
def modern():
    return render_template("modern.html")


@main_bp.route("/math")
def math_tools():
    return render_template("math_tools.html")


@main_bp.route("/attacks")
def attacks():
    return render_template("attacks.html")


# ── Auth Pages ───────────────────────────────────────────────────
@main_bp.route("/login")
def login_page():
    return render_template("login.html")


@main_bp.route("/register")
def register_page():
    return render_template("register.html")


# ── New Feature Pages (v2.0) ────────────────────────────────────
@main_bp.route("/playground")
def playground():
    return render_template("playground.html")


@main_bp.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")


@main_bp.route("/simulator")
def simulator():
    return render_template("simulator.html")


@main_bp.route("/challenges")
def challenges():
    return render_template("challenges.html")


@main_bp.route("/file-crypto")
def file_crypto():
    return render_template("file_crypto.html")


@main_bp.route("/keygen")
def keygen():
    return render_template("keygen.html")


@main_bp.route("/benchmark")
def benchmark():
    return render_template("benchmark.html")


@main_bp.route("/reports")
def reports():
    return render_template("reports.html")


@main_bp.route("/api-docs")
def api_docs():
    return render_template("api_docs.html")


@main_bp.route("/codegen")
def codegen():
    return render_template("codegen.html")


@main_bp.route("/encryption-table")
def encryption_table():
    return render_template("encryption_table.html")


@main_bp.route("/learning")
def learning():
    return render_template("learning.html")
