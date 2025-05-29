# app/db.py

import os
from dotenv   import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_message(chat_id: str, role: str, content: str):
    """
    Сохраняет сообщение в таблицу messages_history:
      chat_id (uuid/text) — из Telegram Update.user.id
      role    (text)     — 'user' или 'assistant'
      content (text)     — само сообщение
      timestamp (timestamptz) — заполняется автоматически
    """
    supabase.table("messages_history").insert({
        "chat_id": chat_id,
        "role":    role,
        "content": content
    }).execute()
