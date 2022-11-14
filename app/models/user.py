from app.database.db import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    quizzes = relationship("Quiz", back_populates="user")
