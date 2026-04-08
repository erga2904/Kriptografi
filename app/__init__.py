"""
CipherLab Application Factory — v2.4
"""
import os
from flask import Flask
from .config import Config
from .extensions import db, csrf, login_manager, bcrypt, limiter


def _init_directories():
    """Lazily initialize directories (cannot be done at module import time on Vercel)."""
    upload_folder = Config.UPLOAD_FOLDER
    instance_dir = os.path.dirname(upload_folder)
    
    for dir_path in [instance_dir, upload_folder]:
        try:
            os.makedirs(dir_path, exist_ok=True)
        except (OSError, IOError, PermissionError) as e:
            # Silently ignore - Vercel has read-only filesystem
            pass


def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )
    app.config.from_object(config_class)

    # Initialize directories lazily
    with app.app_context():
        _init_directories()

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    # ── JSON error handlers for API routes ───────────────────────
    from flask import jsonify as _jsonify, request as _request

    @app.errorhandler(413)
    def request_entity_too_large(e):
        if _request.path.startswith('/api/'):
            return _jsonify({"error": "Ukuran file melebihi batas maksimal"}), 413
        return e

    @app.errorhandler(429)
    def too_many_requests(e):
        if _request.path.startswith('/api/'):
            return _jsonify({"error": "Terlalu banyak permintaan, coba lagi nanti"}), 429
        return e

    @app.errorhandler(500)
    def internal_server_error(e):
        if _request.path.startswith('/api/'):
            return _jsonify({"error": "Terjadi kesalahan server"}), 500
        return e

    # ── Original Blueprints ──────────────────────────────────────
    from .blueprints.main.routes import main_bp
    from .blueprints.auth.routes import auth_bp
    from .blueprints.classical.routes import classical_bp
    from .blueprints.modern.routes import modern_bp
    from .blueprints.math_tools.routes import math_bp
    from .blueprints.attacks.routes import attacks_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(classical_bp, url_prefix="/api/classical")
    app.register_blueprint(modern_bp, url_prefix="/api/modern")
    app.register_blueprint(math_bp, url_prefix="/api/math")
    app.register_blueprint(attacks_bp, url_prefix="/api/attacks")

    # ── New Feature Blueprints (v2.0) ────────────────────────────
    from .blueprints.playground.routes import playground_bp
    from .blueprints.analyzer.routes import analyzer_bp
    from .blueprints.simulator.routes import simulator_bp
    from .blueprints.challenges.routes import challenges_bp
    from .blueprints.file_crypto.routes import file_crypto_bp
    from .blueprints.keygen.routes import keygen_bp
    from .blueprints.benchmark.routes import benchmark_bp
    from .blueprints.reports.routes import reports_bp
    from .blueprints.api_docs.routes import api_docs_bp
    from .blueprints.codegen.routes import codegen_bp

    app.register_blueprint(playground_bp, url_prefix="/api/playground")
    app.register_blueprint(analyzer_bp, url_prefix="/api/analyzer")
    app.register_blueprint(simulator_bp, url_prefix="/api/simulator")
    app.register_blueprint(challenges_bp, url_prefix="/api/challenges")
    app.register_blueprint(file_crypto_bp, url_prefix="/api/file-crypto")
    app.register_blueprint(keygen_bp, url_prefix="/api/keygen")
    app.register_blueprint(benchmark_bp, url_prefix="/api/benchmark")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(api_docs_bp, url_prefix="/api/docs")
    app.register_blueprint(codegen_bp, url_prefix="/api/codegen")

    # Create database tables
    with app.app_context():
        try:
            from . import models  # noqa: F401
            db.create_all()
        except Exception as e:
            app.logger.warning(f"Could not create database tables: {e}")

    # CSRF exemption for all API routes
    api_blueprints = [
        classical_bp, modern_bp, math_bp, attacks_bp,
        playground_bp, analyzer_bp, simulator_bp, challenges_bp,
        file_crypto_bp, keygen_bp, benchmark_bp, reports_bp,
        api_docs_bp, codegen_bp,
    ]
    for bp in api_blueprints:
        csrf.exempt(bp)

    return app
