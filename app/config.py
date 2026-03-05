"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, '..', 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

UPLOAD_DIR = os.path.join(INSTANCE_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

DB_PATH = os.path.abspath(os.path.join(INSTANCE_DIR, 'cipherlab.db'))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32).hex())
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    UPLOAD_FOLDER = UPLOAD_DIR
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
