# app/handlers.py

from app.calculator import calc_personal_numbers
from app.ai_client   import get_forecast
from app.db          import save_message

async def handle_update(data: dict) -> dict:
    """
    Обрабатывает входящий вебхук от Telegram:
    1) Сохраняет текст пользователя в Supabase
    2) Считает персональные числа
    3) Запрашивает прогноз у OpenAI
    4) Сохраняет ответ бота в Supabase
    5) Возвращает dict с полями chat_id и text
    """
    user_id = str(data["user"]["id"])
    text    = data["message"]["text"]

    # 1) Сохраняем входящее сообщение
    save_message(user_id, "user", text)

    # 2) Считаем личные числа
    numbers = calc_personal_numbers(text)

    # 3) Получаем текст прогноза
    forecast = get_forecast(numbers)

    # 4) Сохраняем ответ бота
    save_message(user_id, "bot", forecast)

    # 5) Отдаём готовый ответ Telegram API
    return {"chat_id": user_id, "text": forecast}
