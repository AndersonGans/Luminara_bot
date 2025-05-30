# app/ai_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict

# подгружаем .env
load_dotenv()

# инициализируем клиент
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# ваш системный промпт
SYSTEM_PROMPT = (
    "Ты — цифровой нумеролог-консультант школы Люминары по имени Василиса. "
    "Используй трёхуровневую систему расчёта личного дня."
)

def get_forecast(numbers: Dict[str,int]) -> str:
    # 1) формируем сообщения
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Расчёты: {numbers}"}
    ]

    # 2) вызываем ChatCompletion с обязательными аргументами
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),  # модель по-умолчанию
        messages=messages,
    )

    # 3) возвращаем текст прогноза
    return resp.choices[0].message.content.strip()
