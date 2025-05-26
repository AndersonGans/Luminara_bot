# handlers.py
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, Application

from calculator import calculate_personal_numbers  # ваш калькулятор

def register_handlers(app: Application):
    # перехватываем любые текстовые сообщения (не команды)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # 1) попробуем распарсить дату в формате ДД.ММ.ГГГГ
    m = re.match(r"^(\d{2})\.(\d{2})\.(\d{4})$", text)
    if not m:
        # если не дата — просто отвечаем шаблонно
        return await update.message.reply_text("Введите дату рождения в формате ДД.ММ.ГГГГ")
    
    day, month, year = map(int, m.groups())

    # 2) считаем все необходимые числа
    nums = calculate_personal_numbers(day, month, year)
    # nums будет dict вида:
    # { "year": 9, "month": 5, "day": 4, "personal": 5, "perception": 7, ... }

    # 3) подготавливаем prompt для GPT-ассистента
    prompt = (
        f"Пользователь родился {day:02d}.{month:02d}.{year}. "
        f"Рассчитанные показатели: "
        f"Личный год = {nums['year']}, "
        f"Личный месяц = {nums['month']}, "
        f"Личный день = {nums['day']}, "
        f"Число личности = {nums['personal']}, "
        f"Число восприятия = {nums['perception']}. "
        "Дайте подробную нумерологическую трактовку каждого из этих чисел."
    )

    # 4) берём из bot_data OpenAI-клиент и ID ассистента
    client_oa    = context.bot_data["OPENAI_CLIENT"]
    assistant_id = context.bot_data["ASSISTANT_ID"]

    # 5) отправляем запрос в OpenAI
    resp = client_oa.chat.completions.create(
        assistant=assistant_id,
        messages=[
            {"role": "system", "content": "Ты — нумеролог-ассистент, даёшь развёрнутые толкования."},
            {"role": "user",   "content": prompt}
        ]
    )

    answer = resp.choices[0].message.content

    # 6) шлём результат пользователю
    await update.message.reply_text(answer)
