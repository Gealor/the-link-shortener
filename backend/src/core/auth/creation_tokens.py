import hashlib
import secrets


def hash_token(token: str) -> str:
    hash_bytes = hashlib.sha256(token.encode("utf-8"))  # быстрая операция, очень быстрая
    return hash_bytes.hexdigest()


def create_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)
    return token, token_hash
