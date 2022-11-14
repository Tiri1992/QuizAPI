from abc import ABC, abstractmethod
from fastapi import HTTPException, status


class DBAbstract(ABC):
    @abstractmethod
    def commit(self):
        pass


class TransactionHandler(ABC):
    @abstractmethod
    def apply(self):
        pass


class ValidationHandler(ABC):
    @abstractmethod
    def apply(self):
        pass


class UserDB(DBAbstract):
    def __init__(
        self,
        transaction_handler: TransactionHandler,
        validation_handler: ValidationHandler,
    ) -> None:
        self._transaction_handler = transaction_handler
        self._validation_handler = validation_handler

    def commit(self):
        self._validation_handler.apply()
        return self._transaction_handler.apply()


class QuizDB(DBAbstract):
    def __init__(
        self,
        transaction_handler: TransactionHandler,
        validation_handler: ValidationHandler,
    ) -> None:
        self._transaction_handler = transaction_handler
        self._validation_handler = validation_handler

    def commit(self):
        self._validation_handler.apply()
        return self._transaction_handler.apply()


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


class ReadSingleHandler(TransactionHandler):
    def __init__(self, db, model, _id) -> None:
        self._db = db
        self._model = model
        self._id = _id

    def apply(self):
        return (
            self._db.query(self._model)
            .filter(self._model.id == self._id)
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


class ValidateUserExists(ValidationHandler):
    # TODO: Finish implementation
    def __init__(self, db, model, email) -> None:
        self._db = db
        self._model = model
        self._email = email

    def apply(self):
        return super().apply()


class ValidateUserNotExists(ValidationHandler):
    # TODO: Finish implementation
    def __init__(self, db, model, email) -> None:
        self._db = db
        self._model = model
        self._email = email

    def apply(self):
        res = (
            self._db.query(self._model)
            .filter(self._model.email == self._email)
            .first()
        )
        if res:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {self._email} already exists.",
            )
