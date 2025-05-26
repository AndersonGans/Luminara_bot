import os
from supabase import create_client
from openai import OpenAI
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

from calculator import calculate_personal_numbers

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
openai = OpenAI(api_key=os.getenv("OPENAI_KEY"))

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()
    try:
        day, month, year = map(int, text.split('.'))
    except ValueError:
        await update.message.reply_text("Введите дату в формате ДД.MM.ГГГГ")
        return

    dob = f"{year:04d}-{month:02d}-{day:02d}"
#    supabase.table("users").upsert({
#        "id": user.id,
#       "username": user.username or "",
#        "date_of_birth": dob
#    }).execute()

    nums = calculate_personal_numbers(day, month, year)
    reply = (
        f"Привет, {user.first_name}!\n"
        f"Число восприятия: {nums['perception']} {nums['perception_symbol']}\n"
        f"Число личности: {nums['personality']} {nums['personality_symbol']}\n"
        f"Личный год: {nums['year']} {nums['year_symbol']}\n"
        f"Личный месяц: {nums['month']} {nums['month_symbol']}\n"
        f"Личный день: {nums['day']} {nums['day_symbol']}"
    )
    await update.message.reply_text(reply)

def register_handlers(app):
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_message)
    )
