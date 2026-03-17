from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
import crud
import api_client
from database import engine, Base, get_db
# from app.models import Question  # этот импорт не нужен, если не используется напрямую
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Quiz Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/api/questions", response_model=schemas.QuestionOut | dict)
async def receive_questions(
    request: schemas.QuestionsNum,
    db: AsyncSession = Depends(get_db)
):
    n = request.questions_num
    if n <= 0:
        raise HTTPException(status_code=400, detail="questions_num must be positive")

    last_question_before = await crud.get_last_question(db)
    questions_from_api = await api_client.fetch_questions(n)

    saved_questions = []
    for i in range(n):
        if i >= len(questions_from_api):
            new_q = await api_client.fetch_questions(1)
            if new_q:
                questions_from_api.append(new_q[0])
            else:
                logger.warning("API не вернул вопрос, пропускаем итерацию")
                continue

        current_question = questions_from_api[i]
        existing = await crud.get_question_by_id(db, current_question["id"])
        while existing:
            logger.info(f"Вопрос с id {current_question['id']} уже существует, запрашиваем новый")
            new_q = await api_client.fetch_questions(1)
            if not new_q:
                break
            current_question = new_q[0]
            existing = await crud.get_question_by_id(db, current_question["id"])

        if not existing:
            saved = await crud.create_question(db, current_question)
            saved_questions.append(saved)
        else:
            logger.error("Не удалось получить уникальный вопрос после нескольких попыток")

    if last_question_before:
        return schemas.QuestionOut.model_validate(last_question_before)
    else:
        return {}