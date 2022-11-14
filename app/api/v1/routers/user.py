from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserRequest
from app.api.deps import get_db
from app.core.services import UserDB, CreateHandler, ValidateUserNotExists
from app.models.user import User

user_router = APIRouter(
    prefix="/users",
    tags=["USER"],
)


@user_router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(body: UserRequest, db: Session = Depends(get_db)):
    handler = CreateHandler(
        db=db,
        model=User,
        schema=body,
    )
    validation = ValidateUserNotExists(
        db=db,
        model=User,
        email=body.email,
    )
    user_db = UserDB(
        transaction_handler=handler,
        validation_handler=validation,
    )
    return user_db.commit()
