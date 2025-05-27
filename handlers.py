# handlers.py
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from calculator import calculate_personal_numbers  # <-- вот эта функция теперь есть!

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите дату в формате ДД.MM.ГГГГ")

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    # простая проверка формата ДД.MM.ГГГГ
    try:
        d, m, y = map(int, text.split("."))
    except:
        return await update.message.reply_text("Неверный формат, попробуйте ДД.MM.ГГГГ")

    nums = calculate_personal_numbers(d, m, y)

    resp = (
        f"Привет, {update.effective_user.first_name}!\n"
        f"Число восприятия: {nums['perception']} {nums['perception_symbol']}\n"
        f"Число личности: {nums['personality']} {nums['personality_symbol']}\n"
        f"Личный год: {nums['year']} {nums['year_symbol']}\n"
        f"Личный месяц: {nums['month']} {nums['month_symbol']}\n"
        f"Личный день: {nums['day']} {nums['day_symbol']}"
    )
    await update.message.reply_text(resp)

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
