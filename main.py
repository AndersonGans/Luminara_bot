import os
from dotenv import load_dotenv

# 1) Сразу грузим .env
load_dotenv()

# 2) Достаем все нужные ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY     = os.getenv("OPENAI_KEY")
ASSISTANT_ID   = os.getenv("ASSISTANT_ID")

for name, val in (("TELEGRAM_TOKEN", TELEGRAM_TOKEN),
                  ("OPENAI_KEY", OPENAI_KEY),
                  ("ASSISTANT_ID", ASSISTANT_ID)):
    if not val:
        print(f"Ошибка: {name} не задан")
        exit(1)

# 3) Инициализируем OpenAI-клиент
from openai import OpenAI
client_oa = OpenAI(api_key=OPENAI_KEY)

# 4) Telegram-бот
from telegram.ext import Application
from handlers import register_handlers

def main():
    # строим приложение
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # сохраняем OpenAI-клиент и ID ассистента в bot_data
    app.bot_data["OPENAI_CLIENT"] = client_oa
    app.bot_data["ASSISTANT_ID"]  = ASSISTANT_ID

    register_handlers(app)

    print("🤖 Бот запущен и слушает сообщения...")

    # Сбрасываем все webhook и дропаем старые getUpdates, чтобы не было конфликтов
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
