import asyncio

import bcrypt


async def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode("utf-8")
    return await asyncio.to_thread(bcrypt.hashpw, pwd_bytes, salt)
# bcrypt имеет относительно медленные и тяжеловесные операции, также является C-расширением,
# поэтому GIL отпускается и есть смысл уносить вызов в отдельный поток


async def compare_hashed_passwords(
    entered_password: bytes,
    hashed_password: bytes,
) -> bool:
    return await asyncio.to_thread(bcrypt.checkpw, entered_password, hashed_password)
