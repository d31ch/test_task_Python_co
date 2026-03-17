from pydantic import BaseModel
from datetime import datetime

class QuestionsNum(BaseModel):
    questions_num: int

class QuestionOut(BaseModel):
    id: int
    question_text: str
    answer_text: str
    created_at: datetime

    class Config:
        from_attributes = True