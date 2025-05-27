# handlers.py
import re
import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from calculator import calculate_personal_numbers

# фильтр: принимаем любые текстовые сообщения
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    # ищем D.D.YYYY
    m = re.match(r'(\d{2})\.(\d{2})\.(\d{4})', text)
    if not m:
        # если не дата, просто игнорируем или можно ответить подсказкой
        return

    day, month, year = map(int, m.groups())
    nums = calculate_personal_numbers(day, month, year)
    # nums = {'year':…, 'month':…, 'day':…, 'personal':…, 'perception':…, …}

    # Собираем промт для ассистента:
    user_query = f"Пользователь запросил нумерологический анализ для {day:02d}.{month:02d}.{year}.\n"
    user_query += (
        f"Личный год: {nums['year']}, "
        f"Личный месяц: {nums['month']}, "
        f"Личный день: {nums['day']}, "
        f"Число личности: {nums['personal']}, "
        f"Число восприятия: {nums['perception']}.\n\n"
        "Пожалуйста, дай развёрнутый нумерологический прогноз на основе этих чисел."
    )

    # Достаем из bot_data наш OpenAI-клиент и assistant_id
    client_oa = context.bot_data["OPENAI_CLIENT"]
    assistant_id = context.bot_data["ASSISTANT_ID"]

    # Отправляем запрос ассистенту
    resp = await client_oa.chat.completions.create(
        assistant=assistant_id,
        messages=[
            {"role":"system", "content":"Ты нумеролог-ассистент. Работай по данным."},
            {"role":"user",   "content":user_query}
        ]
    )

    answer = resp.choices[0].message.content
    # Шлём пользователю
    await update.message.reply_text(answer)

def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
