import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import requests
from typing import Dict

# ──────────────────────────────────────────────────────────────────────────────
# 1. Явно загружаем переменные из /root/Luminara_bot/.env
# ──────────────────────────────────────────────────────────────────────────────
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

OPENAI_KEY   = os.getenv("OPENAI_KEY")     # Должен быть вида sk-…
ASSISTANT_ID = os.getenv("ASSISTANT_ID")   # Должен быть вида asst_…

# ──────────────────────────────────────────────────────────────────────────────
# 2. Настраиваем простой логгер, чтобы видеть, подхватились ли переменные
# ──────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s:%(lineno)d – %(message)s"
)
logging.info(f"AI_CLIENT: OPENAI_KEY={'YES' if OPENAI_KEY else 'NO'}")
logging.info(f"AI_CLIENT: ASSISTANT_ID={ASSISTANT_ID!r}")

if not OPENAI_KEY:
    raise RuntimeError("Не найдена переменная OPENAI_KEY в окружении.")
if not ASSISTANT_ID:
    raise RuntimeError("Не найдена переменная ASSISTANT_ID в окружении.")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Системный промпт (по нему Luminara-ассистент строит прогноз)
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "Ты — цифровой нумеролог-консультант школы Люминары по имени Василиса. "
    "Используй трёхуровневую систему расчёта личного дня, "
    "не показывай подробных вычислений, сразу выдавай готовый прогноз с лёгкой иронией."
)

# ──────────────────────────────────────────────────────────────────────────────
# 4. URL Assistants API
# ──────────────────────────────────────────────────────────────────────────────
ASSISTANT_ENDPOINT = f"https://api.openai.com/v1/assistants/{ASSISTANT_ID}/chat/completions"

# ──────────────────────────────────────────────────────────────────────────────
# 5. Функция для запроса прогноза
# ──────────────────────────────────────────────────────────────────────────────
def get_forecast(numbers: Dict[str, int]) -> str:
    """
    Формирует HTTP-запрос к Assistants API и возвращает текст прогноза.
    Если произошла ошибка — возвращает понятное сообщение.
    """
    # 5.1. Формируем сообщения
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Расчёты: {numbers}"}
    ]

    # 5.2. Заголовки — ключ и специальный header для Assistants API
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }

    # 5.3. Тело запроса
    payload = {
        "messages": messages
    }

    try:
        # 5.4. Делаем POST-запрос
        response = requests.post(ASSISTANT_ENDPOINT, headers=headers, json=payload, timeout=30)
    except Exception as e:
        logging.exception(f"Непредвиденная ошибка при HTTP-запросе к Assistants API: {e!r}")
        return "❗ Внутренняя ошибка при обращении к OpenAI. Попробуйте ещё раз."

    # 5.5. Если HTTP-код не 200, значит что-то не так (ключ, ID или права)
    if response.status_code != 200:
        try:
            # попытаемся распарсить тело ошибки как JSON
            data = response.json()
            error_msg = data.get("error", {}).get("message", "<No message>")
        except Exception:
            error_msg = response.text or f"HTTP {response.status_code}"
        logging.error(f"Ошибка от OpenAI Assistants API: HTTP {response.status_code}: {error_msg!r}")
        # В зависимости от текста ошибки, вы поймёте, что делать дальше:
        #  - Authentication error → ключ неправильный или просрочен
        #  - assistant is not published → нужно зайти на платформу и нажать Publish у ассистента
        #  - You do not have access → ключ не из той организации
        return f"❗ Ошибка от OpenAI: {error_msg}. Проверьте настройки ключа/ассистента."

    # 5.6. Если HTTP 200, парсим JSON и возвращаем содержимое
    try:
        result = response.json()
        # ожидаем, что result["choices"][0]["message"]["content"] содержит текст
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.exception(f"Не удалось распарсить ответ от OpenAI: {e!r} / ответ: {response.text!r}")
        return "❗ Неверный формат ответа от OpenAI. Попробуйте позже."
