from passlib.context import CryptContext


def hash_password(password: str, algorithm: str) -> str:
    crypt = CryptContext(
        schemes=[algorithm],
        deprecated="auto",
    )
    return crypt.hash(password)


def validate_hash_password(
    password_to_validate: str, password_hashed: str, algorithm: str
) -> bool:
    crypt = CryptContext(
        schemes=[algorithm],
        deprecated="auto",
    )
    return crypt.verify(password_to_validate, password_hashed)
