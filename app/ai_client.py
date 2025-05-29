import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_KEY   = os.getenv("OPENAI_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = (
    "Ты — ассистент Наука Luminara, эксперт в нумерологии. "
    "У тебя есть база знаний по системе Luminara. "
    "Отвечай с лёгкой иронией, не показывай расчёты, "
    "давай только готовый прогноз."
)

def get_forecast(данные: dict) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Расчёты:\n{данные}"}
    ]
    resp = client.chat.completions.create(
        assistant=ASSISTANT_ID,
        model="gpt-3.5-turbo",
        messages=messages
    )
    return resp.choices[0].message.content.strip()
