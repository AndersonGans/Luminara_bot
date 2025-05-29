# app/db.py

import os
from dotenv   import load_dotenv
from supabase import create_client

# Загружаем .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_message(user_id: str, role: str, content: str):
    """
    Сохраняет сообщение в таблицу messages_history:
      - user_id   (text)
      - role      (text, 'user' или 'assistant')
      - content   (text)
      - timestamp (техническое поле timestamptz по умолчанию)
    """
    supabase.table("messages_history").insert({
        "user_id": user_id,
        "role":    role,
        "content": content
    }).execute()
