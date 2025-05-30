# app/ai_client.py
import os
from openai import OpenAI
from typing import Dict

# Инициализируем клиент
client = OpenAI(
    api_key=os.getenv("OPENAI_KEY"),     # ваш sk-ключ
    # Если у вас есть приватная инстанс-модель (Assistant), 
    # вместо model= передавайте assistant=os.getenv("ASSISTANT_ID")
)

def get_forecast(numbers: Dict[str,int]) -> str:
    """
    Делает запрос к OpenAI ChatCompletion и возвращает прогноз.
    ВАЖНО: здесь передаются оба обязательных аргумента — model (или assistant) и messages.
    """
    # 1) Формируем цепочку сообщений согласно вашему системному промпту
    system_msg = {
        "role": "system",
        "content": (
            "Ты — цифровой нумеролог-консультант школы Люминары по имени Василиса. "
            "Используй трёхуровневую систему расчёта личного дня."
        ),
    }
    # 2) Пользовательский запрос с числами
    user_msg = {
        "role": "user",
        "content": f"Мои персональные числа: день={numbers['day']}, "
                   f"месяц={numbers['month']}, год={numbers['year']}. "
                   "Дай краткий прогноз на сегодня.",
    }

    # 3) Запускаем ChatCompletion
    resp = client.chat.completions.create(
        # Если вы хотите использовать стандартную модель:
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        # — или, если вы хотите использовать ваш Assistant из UI:
        # assistant=os.getenv("ASSISTANT_ID"),
        messages=[system_msg, user_msg],
    )

    # 4) Достаём текст ответа
    return resp.choices[0].message.content
