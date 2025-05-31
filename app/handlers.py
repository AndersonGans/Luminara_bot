import logging
from app.calculator import calc_personal_numbers
from app.ai_client   import get_forecast
from app.db          import save_message

# ──────────────────────────────────────────────────────────────────────────────
# Если нужно, настроим простой логгер:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s:%(lineno)d – %(message)s"
)

async def handle_update(data: dict) -> dict:
    """
    Обрабатывает входящий вебхук от Telegram:
      1) Сохраняет текст пользователя в Supabase
      2) Пытается распарсить дату и посчитать личные числа
      3) Просит прогноз у OpenAI (через Assistants API)
      4) Сохраняет ответ бота в Supabase
      5) Возвращает dict с полями chat_id и text
    """
    # 1) Извлекаем ID и текст
    user_id = str(data.get("user", {}).get("id", ""))   # безопасный геттер
    text    = data.get("message", {}).get("text", "")

    # Если не удалось получить chat_id или text, логируем и возвращаем «400»: 
    # но поскольку FastAPI ожидает dict, мы просто вернём текст об ошибке.
    if not user_id or not text:
        logging.warning(f"handle_update: неверный формат data из Telegram: {data!r}")
        return {"chat_id": user_id or "UNKNOWN", "text": "❗ Я получил странные данные от Telegram. Попробуйте ещё раз."}

    # 2) Сохраняем входящее сообщение в Supabase
    try:
        save_message(user_id, "user", text)
    except Exception as e:
        logging.exception(f"Не удалось сохранить входящее сообщение (user) для {user_id}: {e!r}")
        # но мы всё равно идем дальше: даже если не сохранили, попытаемся обработать
        pass

    # 3) Пытаемся распарсить строку как дату “DD.MM.YYYY” и посчитать личные числа
    try:
        numbers = calc_personal_numbers(text)
    except ValueError:
        # Если формат не DD.MM.YYYY, возвращаем понятное сообщение и не отправляем в OpenAI
        return {
            "chat_id": user_id,
            "text": "❗ Неверный формат даты. Пожалуйста, отправьте дату в формате DD.MM.YYYY (например, 16.02.1987)."
        }
    except Exception as e:
        logging.exception(f"Ошибка при вычислении личных чисел для {text}: {e!r}")
        return {
            "chat_id": user_id,
            "text": "❗ Внутренняя ошибка при вычислении чисел. Повторите попытку чуть позже."
        }

    # 4) Получаем прогноз от OpenAI (Assistants API)
    try:
        forecast = get_forecast(numbers)
    except Exception as e:
        # Теоретически get_forecast уже обрабатывает свои ошибки, но на всякий случай:
        logging.exception(f"Ошибка в get_forecast для пользователя {user_id}, numbers={numbers}: {e!r}")
        forecast = "❗ Не удалось сформировать прогноз. Попробуйте чуть позже."

    # 5) Сохраняем ответ ассистента в Supabase
    try:
        save_message(user_id, "assistant", forecast)
    except Exception as e:
        logging.exception(f"Не удалось сохранить ответ ассистента для {user_id}: {e!r}")
        # продолжаем — клиенту всё равно уже отправим текст.

    # 6) Возвращаем словарь с chat_id и текстом
    return {
        "chat_id": user_id,
        "text": forecast
    }
