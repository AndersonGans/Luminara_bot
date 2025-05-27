# handlers.py
import json
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from calculator import calculate_personal_numbers

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    # 1) разбираем дату рождения
    try:
        day, month, year = map(int, text.split("."))
    except:
        await update.message.reply_text("Введите дату в формате ДД.MM.ГГГГ")
        return

    # 2) считаем все свои цифры
    nums = calculate_personal_numbers(day, month, year)
    # 3) сразу шлём пользователю краткий ответ, чтобы он видел, что бот работает
    await update.message.reply_text(
        f"✨ Ваши числа: год={nums['year']}, мес={nums['month']}, день={nums['day']},\n"
        f"личность={nums['personal']}, восприятие={nums['perception']}\n"
        "Сейчас готовлю подробный нумерологический прогноз…"
    )

    # 4) берём из bot_data OpenAI-клиент и assistant_id
    client_oa    = context.bot_data["OPENAI_CLIENT"]
    assistant_id = context.bot_data["ASSISTANT_ID"]

    # 5) собираем сообщение для ассистента
    system = {
        "role": "system",
        "content": (
            "Ты — Luminaria, опытный нумеролог. "
            "Твоя задача — на основе предоставленных цифр дать полный нумерологический прогноз."
        )
    }
    user_msg = {
        "role": "user",
        "content": (
            "Пользователь родился {day}.{month}.{year}. "
            "Его персональные числа: "
            f"Личный год = {nums['year']} ({nums['year_symbol']}), "
            f"Личный месяц = {nums['month']} ({nums['month_symbol']}), "
            f"Личный день = {nums['day']} ({nums['day_symbol']}), "
            f"Число личности = {nums['personal']} ({nums['personal_symbol']}), "
            f"Число восприятия = {nums['perception']} ({nums['perception_symbol']}).\n"
            "Сделай для него подробный прогноз."
        ).format(day=day, month=month, year=year)
    }

    # 6) делаем запрос к вашему ассистенту
    resp = client_oa.chat.completions.create(
        model="gpt-4o-mini",
        assistant_id=assistant_id,
        messages=[system, user_msg],
    )
    answer = resp.choices[0].message["content"]

    # 7) шлём пользователю полный прогноз
    await update.message.reply_text(answer, parse_mode="Markdown")

def register_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
