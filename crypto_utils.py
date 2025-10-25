from cryptography.fernet import Fernet, InvalidToken
from config import Config

def _get_fernet():
    key = Config.ENCRYPTION_KEY
    if isinstance(key, str):
        key_bytes = key.encode()
    else:
        key_bytes = key
    return Fernet(key_bytes)

def encrypt_password(plaintext: str) -> str:
    """
    Encrypt plaintext password and return base64 token string.
    """
    f = _get_fernet()
    token = f.encrypt(plaintext.encode())
    return token.decode()

def decrypt_password(token: str) -> str:
    """
    Decrypt the token and return plaintext password.
    Raises InvalidToken if decryption fails.
    """
    f = _get_fernet()
    try:
        pt = f.decrypt(token.encode())
        return pt.decode()
    except InvalidToken as e:
        raise
