from app.database.db import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship


class Quiz(Base):

    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True)
    question = Column(String(255), unique=True, nullable=False)
    answer = Column(String(255), nullable=False)
    created_by = Column(
        Integer, ForeignKey("user.id", name="FK_user_quiz", ondelete="CASCADE")
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="quizzes")
