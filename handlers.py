# handlers.py
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from calculator import calculate_personal_numbers  # ваш расчёт
from supabase import create_client  # если вы сохраняете данные
from psycopg import sql  # или используете pydantic/postgrest — как у вас устроено

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # 1) Парсим дату ДД.ММ.ГГГГ
    try:
        day, month, year = map(int, text.split('.'))
    except ValueError:
        return await update.message.reply_text("Введите дату в формате ДД.MM.ГГГГ")

    # 2) Считаем все нумерологические числа
    nums = calculate_personal_numbers(day, month, year)
    # nums = {
    #   "year": 9, "month": 5, "day": 4,
    #   "personal": 5, "perception": 7
    # }

    # 3) Формируем промт для ассистента
    prompt = (
        f"Пользователь родился {text}. "
        f"Рассчитаны нумерологические числа:\n"
        f"- Личный год: {nums['year']}\n"
        f"- Личный месяц: {nums['month']}\n"
        f"- Личный день: {nums['day']}\n"
        f"- Число личности: {nums['personal']}\n"
        f"- Число восприятия: {nums['perception']}\n\n"
        "Пожалуйста, дай нумерологический прогноз и разбор этих цифр "
        "в формате дружелюбного сообщения пользователю."
    )

    # 4) Вызываем вашего ассистента
    client_oa: "OpenAI" = context.bot_data["OPENAI_CLIENT"]
    assistant_id: str = context.bot_data["ASSISTANT_ID"]

    resp = await client_oa.chat.completions.create(
        model="gpt-4o-mini",
        assistant=assistant_id,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    reply = resp.choices[0].message.content

    # 5) Отправляем ответ пользователю
    await update.message.reply_text(reply)

def register_handlers(app):
    # Убираем все старые обработчики, ставим один общий
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
