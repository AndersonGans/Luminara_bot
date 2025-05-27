# handlers.py

import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler, Application
from calculator import calculate_personal_numbers

# Регулярка для даты в формате ДД.ММ.ГГГГ
DATE_RE = re.compile(r"^(\d{2})\.(\d{2})\.(\d{4})$")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я нумерологический бот.\n"
        "Отправь мне дату рождения в формате ДД.MM.ГГГГ — и я дам тебе прогноз."
    )

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    m = DATE_RE.match(text)
    if not m:
        return  # не дата — игнорим

    day, month, year = map(int, m.groups())
    nums = calculate_personal_numbers(day, month, year)

    # Формируем текст для ассистента
    calc_text = (
        f"Личный год: {nums['year']}\n"
        f"Личный месяц: {nums['month']}\n"
        f"Личный день: {nums['day']}\n"
        f"Число личности: {nums['personality']}\n"
        f"Число восприятия: {nums['perception']}"
    )
    user_prompt = (
        f"Пользователь родился {day:02d}.{month:02d}.{year}.\n"
        f"Мы рассчитали следующие показатели:\n{calc_text}\n\n"
        "Дай развёрнутое нумерологическое толкование каждого пункта."
    )

    # Достаём OpenAI-клиент и ID ассистента из bot_data
    client_oa   = context.bot_data["OPENAI_CLIENT"]
    assistant   = context.bot_data["ASSISTANT_ID"]

    # Запрашиваем прогноз у вашего ассистента
    resp = await client_oa.chat.completions.create(
        model="gpt-4o-mini",
        assistant=assistant,
        messages=[
            {"role": "system", "content": "Ты — нумеролог-ассистент, даёшь осмысленные прогнозы."},
            {"role": "user",   "content": user_prompt}
        ]
    )

    answer = resp.choices[0].message.content
    await update.message.reply_text(answer)

def register_handlers(app: Application):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_message)
    )
