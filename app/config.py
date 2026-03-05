"""
Application Configuration
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Support either local instance dir or /tmp for Vercel
IS_VERCEL = os.environ.get("VERCEL") == "1"
if IS_VERCEL or os.environ.get("DATABASE_URL"):
    INSTANCE_DIR = "/tmp"
else:
    INSTANCE_DIR = os.path.join(BASE_DIR, '..', 'instance')

# DON'T create directories here - it fails on Vercel read-only filesystem
# Directories will be created lazily in app context

UPLOAD_DIR = os.path.join(INSTANCE_DIR, 'uploads')

# Build database path with proper format for SQLAlchemy
DB_PATH = os.path.abspath(os.path.join(INSTANCE_DIR, 'cipherlab.db'))
# SQLite URI: use sqlite:/// for absolute paths
if sys.platform == 'win32':
    # Windows: sqlite:///C:/path/to/db.db
    DB_URI = f"sqlite:///{DB_PATH}".replace('\\', '/')
else:
    # Unix: sqlite:////absolute/path/to/db.db
    DB_URI = f"sqlite:///{DB_PATH}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32).hex())
    
    # Support PostgreSQL for production, SQLite for development
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = DB_URI
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    UPLOAD_FOLDER = UPLOAD_DIR
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
