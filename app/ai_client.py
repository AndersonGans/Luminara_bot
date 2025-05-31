import os
import logging
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from typing import Dict

# ──────────────────────────────────────────────────────────────────────────────
# 1. Загружаем переменные из .env
# ──────────────────────────────────────────────────────────────────────────────
load_dotenv()

OPENAI_KEY   = os.getenv("OPENAI_KEY")     # должен быть sk-proj-...
ASSISTANT_ID = os.getenv("ASSISTANT_ID")   # должен быть вида asst_...

if not OPENAI_KEY:
    raise RuntimeError("Не найдена переменная OPENAI_KEY в окружении.")
if not ASSISTANT_ID:
    raise RuntimeError("Не найдена переменная ASSISTANT_ID в окружении.")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Инициализируем OpenAI-клиент (Python-SDK)
# ──────────────────────────────────────────────────────────────────────────────
client = OpenAI(api_key=OPENAI_KEY)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Системный промпт
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "Ты — цифровой нумеролог-консультант школы Люминары по имени Василиса. "
    "Используй трёхуровневую систему расчёта личного дня, не показывай подробных "
    "вычислений, сразу выдавай готовый прогноз с лёгкой иронией."
)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Функция для получения прогноза
# ──────────────────────────────────────────────────────────────────────────────
def get_forecast(numbers: Dict[str, int]) -> str:
    """
    Формирует запрос к кастомному ассистенту (Assistants API)
    и возвращает текст прогноза. При ошибке возвращает понятное сообщение.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Расчёты: {numbers}"}
    ]

    try:
        # ВАЖНО: передаём assistant=ASSISTANT_ID, а не model=…
        resp = client.chat.completions.create(
            assistant=ASSISTANT_ID,
            messages=messages
        )
    except OpenAIError as e:
        logging.error(f"Ошибка при обращении к OpenAI Assistants API: {e!r}")
        return "❗ Извините, сейчас не могу получить прогноз (ошибка OpenAI). Повторите позже."
    except Exception as e:
        logging.exception("Непредвиденная ошибка в get_forecast:")
        return "❗ Произошла внутренняя ошибка при формировании прогноза. Попробуйте ещё раз."

    try:
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logging.exception(f"Не удалось извлечь содержимое ответа OpenAI: {e!r} / ответ: {resp!r}")
        return "❗ Неверный формат ответа от OpenAI. Повторите позже."
