import re
from datetime import date
from telegram.ext import Application, MessageHandler, filters
from calculator import calculate_numbers

# шаблон для даты ДД.MM.ГГГГ
DATE_PATTERN = re.compile(r'(\d{2})\.(\d{2})\.(\d{4})')

async def on_message(update, context):
    text = update.message.text or ""
    m = DATE_PATTERN.search(text)
    if not m:
        # если это не дата — можно проигнорировать или ответить о формате
        await update.message.reply_text("Введите дату в формате ДД.MM.ГГГГ")
        return

    day, month, year = map(int, m.groups())
    nums = calculate_numbers(day, month, year, ref_date=date.today())

    reply = (
        f"Число восприятия: {nums['perception']}\n"
        f"Число личности:   {nums['personality']}\n"
        f"Личный год:        {nums['personal_year']}\n"
        f"Личный месяц:     {nums['personal_month']}\n"
        f"Личный день:       {nums['personal_day']}"
    )
    await update.message.reply_text(reply)

def register_handlers(app: Application):
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_message)
    )
