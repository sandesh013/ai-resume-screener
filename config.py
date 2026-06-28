import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)

    # Base Directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Database URL from .env
    DATABASE_URL = os.getenv("DATABASE_URL")

    # PostgreSQL (Neon) in production, SQLite locally
    if DATABASE_URL:
        # Fix for postgres:// URLs if needed
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace(
            "postgres://",
            "postgresql://"
        )
    else:
        SQLITE_DATABASE = "resume_screening.db"
        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{os.path.join(BASE_DIR, SQLITE_DATABASE)}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"pdf", "docx", "doc"}