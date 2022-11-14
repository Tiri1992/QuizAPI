from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):

    email: EmailStr
    password: str


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):

    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:

        orm_mode = True
