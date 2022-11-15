from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserRequest
from app.api.deps import get_db
from app.core.security import hash_password
from app.core.services import (
    UserDB,
    CreateHandler,
    ValidateNotExists,
    ReadSingleHandler,
)
from app.models.user import User

user_router = APIRouter(
    prefix="/users",
    tags=["USER"],
)


@user_router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(body: UserRequest, db: Session = Depends(get_db)):
    body.password = hash_password(body.password, "bcrypt")
    read_handler = ValidateNotExists(
        handler=ReadSingleHandler(
            db=db,
            model=User,
            identifier_attr="email",
            identifier=body.email,
        ),
        message=f"User with email {body.email} exists.",
    )
    user_read = UserDB(handler=read_handler)
    user_read.commit()
    create_handler = CreateHandler(
        db=db,
        model=User,
        schema=body,
    )
    user_create = UserDB(handler=create_handler)
    return user_create.commit()
