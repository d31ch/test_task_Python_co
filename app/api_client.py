import httpx
from typing import List, Dict, Any
import hashlib

async def fetch_questions(count: int) -> List[Dict[str, Any]]:
    """
    Запрашивает у OpenTDB API указанное количество случайных вопросов.
    Возвращает список словарей с ключами: id, question, answer.
    """
    url = f"https://opentdb.com/api.php?amount={count}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    if data["response_code"] == 0:
        results = data["results"]
        formatted_questions = []
        for q in results:
            # Генерируем числовой ID из текста вопроса (стабильный хеш)
            question_text = q["question"]
            # Используем MD5 для получения детерминированного хеша и преобразуем в целое число
            id_int = int(hashlib.md5(question_text.encode()).hexdigest(), 16) % (10**9)  # ограничим размер
            formatted_q = {
                "id": id_int,
                "question": question_text,
                "answer": q["correct_answer"],
                # Поле created_at не добавляем, так как в crud.py мы используем datetime.utcnow()
            }
            formatted_questions.append(formatted_q)
        return formatted_questions
    else:
        return []