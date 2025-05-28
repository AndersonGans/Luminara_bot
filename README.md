# Luminara Bot

Телеграм-бот и API для персональных нумерологических прогнозов по системе Luminara.

## Стек

- **FastAPI** + **Uvicorn**  
- **Supabase** (PostgreSQL + Auth)  
- **OpenAI** (Chat Completions, кастомный ассистент)  
- **Python 3.10+**, виртуальное окружение `venv`  
- **.env** для хранения токенов и ключей  
- Отправка ответов через Telegram Bot API (`sendMessage`)

## Установка

1. Клонировать репозиторий:
   ```bash
   git clone git@github.com:AndersonGans/Luminara_bot.git
   cd Luminara_bot
