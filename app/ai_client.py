# app/ai_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Загружаем переменные из .env
load_dotenv()

# 2. Читаем ключ и ID ассистента
OPENAI_KEY   = os.getenv("OPENAI_KEY")    # должен быть sk-proj-…
ASSISTANT_ID = os.getenv("ASSISTANT_ID")  # asst_…

# 3. Ваша системная инструкция для ассистента
SYSTEM_PROMPT = (
    "Ты — ассистент Наука Luminara, эксперт в нумерологии. "
    "У тебя есть база знаний по системе Luminara. "
    "Отвечай с лёгкой иронией, не показывай расчёты, "
    "давай только готовый прогноз."
)

# 4. Инициализируем OpenAI-клиент
client = OpenAI(api_key=OPENAI_KEY)

def get_forecast(numbers: dict) -> str:
    """
    Формирует запрос в Assistants API и возвращает текст прогноза.
    
    Параметр:
      numbers — словарь с вашими расчётами.
    
    Возвращает:
      string — содержимое первого сообщения ассистента.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Расчёты: {numbers}"}
    ]

    # Вызов Assistants API (не model=…, а assistant=…)
    resp = client.chat.completions.create(
        assistant=ASSISTANT_ID,
        messages=messages
    )

    # Извлекаем и возвращаем чистый текст ответа
    return resp.choices[0].message.content.strip()
