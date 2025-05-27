# handlers.py
import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from calculator import calculate_personal_numbers

# Состояния нашего диалога
ASK_DATE, ASK_TYPE = range(2)

# Подсказки для пользователя
REQUEST_KEYS = [
    ["Личный год", "Личный месяц"],
    ["Личный день", "Число личности"],
    ["Число восприятия", "Всё сразу"],
]
REQUEST_KB = ReplyKeyboardMarkup(REQUEST_KEYS, one_time_keyboard=True, resize_keyboard=True)

def register_handlers(app):
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)
            ],
            ASK_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_type)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Введи, пожалуйста, свою дату рождения в формате ДД.MM.ГГГГ",
        reply_markup=ReplyKeyboardRemove()
    )
    return ASK_DATE

def is_valid_date(s: str) -> bool:
    try:
        day, month, year = map(int, s.split("."))
        datetime.date(year, month, day)
        return True
    except Exception:
        return False

async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not is_valid_date(text):
        await update.message.reply_text("Неверный формат, попробуй ещё раз: ДД.MM.ГГГГ")
        return ASK_DATE

    # Сохраняем дату рождения
    context.user_data["birth_date"] = text
    await update.message.reply_text(
        "Отлично! Что ты хочешь узнать?\n"
        "- Личный год\n"
        "- Личный месяц\n"
        "- Личный день\n"
        "- Число личности\n"
        "- Число восприятия\n"
        "- Всё сразу",
        reply_markup=REQUEST_KB
    )
    return ASK_TYPE

async def receive_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip().lower()
    bd = context.user_data["birth_date"]
    day, month, year = map(int, bd.split("."))
    nums = calculate_personal_numbers(day, month, year)

    # Формируем системный промпт, передаём только ту часть, что выбрал пользователь
    parts = []
    if choice in ("личный год", "всё сразу"):
        parts.append(f"Личный год: {nums['year']} ({nums['year_symbol']})")
    if choice in ("личный месяц", "всё сразу"):
        parts.append(f"Личный месяц: {nums['month']} ({nums['month_symbol']})")
    if choice in ("личный день", "всё сразу"):
        parts.append(f"Личный день: {nums['day']} ({nums['day_symbol']})")
    if choice in ("число личности", "всё сразу"):
        parts.append(f"Число личности: {nums['personal']} ({nums['personal_symbol']})")
    if choice in ("число восприятия", "всё сразу"):
        parts.append(f"Число восприятия: {nums['perception']} ({nums['perception_symbol']})")

    system_prompt = (
        "Ты — нумерологический ассистент. "
        "Дай развёрнутый прогноз только по этим пунктам:\n\n" +
        "\n".join(parts)
    )

    # достаём клиента и ассистента из bot_data
    client_oa    = context.bot_data["OPENAI_CLIENT"]
    assistant_id = context.bot_data["ASSISTANT_ID"]

    # отправляем в Assistants API
    resp = await client_oa.assistants.chat.completions.create(
        assistant=assistant_id,
        thread_id = context.chat_data.get("thread_id"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": f"Пожалуйста, дай прогноз по «{choice}»."},
        ]
    )
    context.chat_data["thread_id"] = resp.thread_id

    answer = resp.choices[0].message.content
    await update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отмена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
