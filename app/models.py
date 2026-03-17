from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    saved_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Question(id={self.id}, question={self.question_text[:20]})>"