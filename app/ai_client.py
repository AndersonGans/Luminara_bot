# app/ai_client.py

import os
from openai import OpenAI

# Инициализируем клиента с ключом типа sk-proj-…
client = OpenAI(
    api_key=os.getenv("OPENAI_KEY"),  # ваш project key
)

def get_forecast(numbers: dict) -> str:
    """
    Запрашивает прогноз у вашего ассистента.
    Вместо model=... передаём assistant=...
    """
    # Собираем историю сообщений, в т.ч. системную инструкцию
    messages = [
        {"role": "system", "content": os.getenv("SYSTEM_PROMPT", "")},
        {"role": "user",   "content": f"Личные числа: {numbers}. Дай прогноз на сегодня."},
    ]

    # Выполняем вызов Assistants API
    resp = client.chat.completions.create(
        assistant=os.getenv("ASSISTANT_ID"),  # asst_9YDXc…
        messages=messages,
    )

    # Извлекаем и возвращаем текст ответа
return resp.choices[0].message.content
