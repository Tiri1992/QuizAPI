from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from app.core.security import validate_hash_password


class DBAbstract(ABC):
    @abstractmethod
    def commit(self):
        pass


class TransactionHandler(ABC):
    @abstractmethod
    def apply(self):
        pass


class ReadHandler(ABC):
    @abstractmethod
    def apply(self):
        pass


class ReadDecorator(ReadHandler):
    # Implements the same interface it wraps
    pass


class UserDB(DBAbstract):
    def __init__(
        self,
        handler: TransactionHandler | ReadHandler,
    ) -> None:
        self._handler = handler

    def commit(self):
        return self._handler.apply()


class QuizDB(DBAbstract):
    def __init__(
        self,
        handler: TransactionHandler | ReadHandler,
    ) -> None:
        self._handler = handler

    def commit(self):
        return self._handler.apply()


class CreateHandler(TransactionHandler):
    def __init__(self, db, model, schema) -> None:
        self._db = db
        self._model = model
        self._schema = schema

    def apply(self):
        record = self._model(**self._schema.dict())
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record


class ReadSingleHandler(ReadHandler):
    def __init__(self, db, model, identifier_attr, identifier) -> None:
        self._db = db
        self._model = model
        self._identifier_attr = identifier_attr
        self._identifier = identifier

    def apply(self):
        return (
            self._db.query(self._model)
            .filter(
                getattr(self._model, self._identifier_attr) == self._identifier
            )
            .first()
        )


class UpdateHandler(TransactionHandler):
    # TODO: Finish implementation
    def __init__(self, db, model) -> None:
        self._db = db
        self._model = model

    def apply(self):
        return super().apply()


class DeleteHandler(TransactionHandler):
    # TODO: Finish implementation
    def __init__(self, db, model) -> None:
        self._db = db
        self._model = model

    def apply(self):
        return super().apply()


class ValidateExists(ReadDecorator):
    def __init__(self, handler: ReadHandler, message: str) -> None:
        self._handler = handler
        self._message = message

    def apply(self):
        res = self._handler.apply()
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self._message,
            )
        return res


class ValidateNotExists(ReadDecorator):
    def __init__(self, handler: ReadHandler, message: str) -> None:
        # Takes in the same interface it wraps
        self._handler = handler
        self._message = message

    def apply(self):
        res = self._handler.apply()
        if res:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=self._message,
            )
        return res


class ValidatePassword(ReadDecorator):
    def __init__(
        self, handler: ReadHandler, message: str, password: str
    ) -> None:
        self._handler = handler
        self._message = message
        self._password = password

    def apply(self):
        res = self._handler.apply()
        if not validate_hash_password(self._password, res.password, "bcrypt"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=self._message,
            )
        return res
