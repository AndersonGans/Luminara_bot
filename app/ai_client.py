# app/ai_client.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Подгружаем ключи из .env
load_dotenv()
OPENAI_KEY   = os.getenv("OPENAI_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Инициализируем клиент
client = OpenAI(api_key=OPENAI_KEY)

# Системный промт для вашей «Науки Luminara»
SYSTEM_PROMPT = (
    "Ты — ассистент Наука Luminara, эксперт в нумерологии. "
    "У тебя есть база знаний по системе Luminara. "
    "Отвечай с лёгкой иронией, не показывай расчёты, "
    "давай только готовый прогноз."
)

def get_forecast(данные: dict) -> str:
    """
    Формирует запрос в OpenAI по готовым расчётам.
    
    Параметр:
      данные — словарь с ключами:
        личный_год, личный_месяц, личный_день,
        число_личности, число_восприятия

    Возвращает:
      строку с текстом прогноза.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Расчёты:\n{данные}"}
    ]
    # Используем ваш кастомный ассистент из Dashbord
    resp = client.chat.completions.create(
        assistant=ASSISTANT_ID,
        messages=messages
    )
    return resp.choices[0].message.content.strip()
