from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Question
import schemas
from datetime import datetime

async def get_question_by_id(db: AsyncSession, question_id: int) -> Question | None:
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()

async def create_question(db: AsyncSession, question_data: dict) -> Question:
    question = Question(
        id=question_data["id"],
        question_text=question_data["question"],
        answer_text=question_data["answer"],
        created_at=datetime.utcnow()  # Используем текущее время сервера
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question

async def get_last_question(db: AsyncSession) -> Question | None:
    result = await db.execute(
        select(Question).order_by(Question.saved_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()