from cryptography.fernet import Fernet, InvalidToken
from app.config import ENCRYPTION_KEY

cipher = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)


def encrypt_password(password: str) -> str:
    """Encripta una contraseña usando Fernet."""
    try:
        return cipher.encrypt(password.encode()).decode()
    except Exception as e:
        raise ValueError(f"Error al encriptar contraseña: {str(e)}") from e


def decrypt_password(encrypted_password: str) -> str:
    """Desencripta una contraseña usando Fernet."""
    try:
        return cipher.decrypt(encrypted_password.encode()).decode()
    except InvalidToken as e:
        raise ValueError(f"Error al desencriptar contraseña: token inválido") from e
    except Exception as e:
        raise ValueError(f"Error al desencriptar contraseña: {str(e)}") from e