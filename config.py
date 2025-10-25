import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'vault.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Encryption key: 44-character base64 key used by Fernet
    ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
    if not ENCRYPTION_KEY:
        # WARNING: For production, set this via environment (or better, a KMS).
        # The app will still run with a generated key but don't use it for production.
        from cryptography.fernet import Fernet
        print("WARNING: ENCRYPTION_KEY not set — generating ephemeral key (do NOT use in production).")
        ENCRYPTION_KEY = Fernet.generate_key().decode()

    # Mail Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() in ['true', '1', 'yes']
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False").lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", os.environ.get("MAIL_USERNAME"))
