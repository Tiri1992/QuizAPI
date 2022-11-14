from typing import Generator
from app.database.db import session_local


def get_db() -> Generator:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
