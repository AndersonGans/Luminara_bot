# handlers.py
import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from calculator import calculate_personal_numbers

def register_handlers(app):
    # Ловим любые текстовые сообщения (не команды)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_message)
    )

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Проверяем — это ли дата?
    if not is_date(text):
        await update.message.reply_text("Введите дату в формате ДД.MM.ГГГГ")
        return

    # Парсим дату
    day, month, year = map(int, text.split('.'))
    nums = calculate_personal_numbers(day, month, year)

    # Формируем системный промпт для ассистента
    system_prompt = (
        "Ты — нумерологический ассистент. "
        "Твоя задача — на основе переданных чисел составить подробный нумерологический прогноз.\n\n"
        f"Личный год: {nums['year']} ({nums['year_symbol']})\n"
        f"Личный месяц: {nums['month']} ({nums['month_symbol']})\n"
        f"Личный день: {nums['day']} ({nums['day_symbol']})\n"
        f"Число личности: {nums['personal']} ({nums['personal_symbol']})\n"
        f"Число восприятия: {nums['perception']} ({nums['perception_symbol']})\n\n"
        "Дай развёрнутый и понятный прогноз, объяснив каждое из этих чисел."
    )

    # Небольшой «тайпинг…» в чате
    await update.message.chat_action("typing")

    # Достаём OpenAI-клиент и ID ассистента
    client_oa   = context.bot_data["OPENAI_CLIENT"]
    assistant_id = context.bot_data["ASSISTANT_ID"]

    # Отправляем сообщение в Assistants API
    resp = await client_oa.assistants.chat.completions.create(
        assistant=assistant_id,
        thread_id = context.chat_data.get("thread_id"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": "Пожалуйста, сделай прогноз на основе этих данных."},
        ]
    )
    # Сохраняем thread_id, чтобы продолжать тот же тред
    context.chat_data["thread_id"] = resp.thread_id

    # Отправляем ответ ассистента пользователю
    assistant_msg = resp.choices[0].message.content
    await update.message.reply_text(assistant_msg)

def is_date(s: str) -> bool:
    parts = s.split('.')
    if len(parts) != 3:
        return False
    day, month, year = parts
    return day.isdigit() and month.isdigit() and year.isdigit()
