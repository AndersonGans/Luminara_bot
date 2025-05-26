import os
from dotenv import load_dotenv

# 1) Сразу грузим .env
load_dotenv()

# 2) Достаем все нужные ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY     = os.getenv("OPENAI_KEY")
ASSISTANT_ID   = os.getenv("ASSISTANT_ID")

if not TELEGRAM_TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан")
    exit(1)
if not OPENAI_KEY:
    print("Ошибка: OPENAI_KEY не задан")
    exit(1)
if not ASSISTANT_ID:
    print("Ошибка: ASSISTANT_ID не задан")
    exit(1)

# 3) Инициализируем OpenAI-клиент
from openai import OpenAI
client_oa = OpenAI(api_key=OPENAI_KEY)

# 4) Telegram-бот
from telegram.ext import Application
from handlers import register_handlers

def main():
    # Строим приложение и передаем туда клиент_oa, ASSISTANT_ID через context.bot_data
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    # кладем OpenAI-клиент и ID ассистента в bot_data, чтобы хендлеры их достали
    app.bot_data["OPENAI_CLIENT"]  = client_oa
    app.bot_data["ASSISTANT_ID"]   = ASSISTANT_ID

    register_handlers(app)

    print("🤖 Бот запущен и слушает сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
