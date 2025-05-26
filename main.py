import os
from dotenv import load_dotenv
from telegram.ext import Application
from handlers import register_handlers

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Ошибка: TELEGRAM_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    register_handlers(app)
    print("🤖 Бот запущен и слушает сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
