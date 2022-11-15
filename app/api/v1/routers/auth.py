from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.api.deps import get_db
from app.core.services import (
    UserDB,
    ReadSingleHandler,
    ValidateExists,
    ValidatePassword,
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["AUTH"],
)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    read_handler = ValidatePassword(
        ValidateExists(
            handler=ReadSingleHandler(
                db=db,
                model=User,
                identifier_attr="email",
                identifier=credentials.username,
            ),
            message=f"User with email {credentials.username} does not exist.",
        ),
        message="Either username or password is incorrect.",
        password=credentials.password,
    )
    user_read = UserDB(handler=read_handler)
    user_read.commit()

    return {
        "login": "Successful",
    }
