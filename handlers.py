import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# Предполагается, что calculate_personal_numbers возвращает dict с числами
from calculator import calculate_personal_numbers

def register_handlers(app):
    # ловим любые текстовые сообщения
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_message)
    )

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # если не дата — можно сразу выходить или приветствовать
    if not is_date(text):
        await update.message.reply_text("Введите дату в формате ДД.MM.ГГГГ")
        return

    day, month, year = map(int, text.split('.'))
    nums = calculate_personal_numbers(day, month, year)

    # готовим контекст для ассистента
    user_id = update.effective_user.id
    # формируем системную часть, чтобы ассистент знал, что делать
    system_prompt = (
        "Ты нумерологический ассистент. "
        "Твоя задача: на основе чисел дать подробный нумерологический прогноз.\n\n"
        f"Пользователь: {user_id}\n"
        f"Личный год: {nums['year']} ({nums['year_symbol']})\n"
        f"Личный месяц: {nums['month']} ({nums['month_symbol']})\n"
        f"Личный день: {nums['day']} ({nums['day_symbol']})\n"
        f"Число личности: {nums['personal']} ({nums['personal_symbol']})\n"
        f"Число восприятия: {nums['perception']} ({nums['perception_symbol']})\n\n"
        "Сделай Пользователю полный нумерологический прогноз на основе этих данных."
    )

    # достаём OpenAI клиента и ID ассистента
    client_oa: "OpenAI" = context.bot_data["OPENAI_CLIENT"]
    assistant_id: str      = context.bot_data["ASSISTANT_ID"]

    # отправляем запрос в Assistants API
    resp = await client_oa.assistants.chat.completions.create(
        assistant=assistant_id,
        messages=[
            {"role": "system",  "content": system_prompt},
            {"role": "user",    "content": "Что скажешь?"}
        ]
    )

    # извлекаем ответ ассистента
    assistant_msg = resp.choices[0].message.content

    # отправляем пользователю
    await update.message.reply_text(assistant_msg)


def is_date(s: str) -> bool:
    parts = s.split('.')
    if len(parts) != 3:
        return False
    day, month, year = parts
    return day.isdigit() and month.isdigit() and year.isdigit()
