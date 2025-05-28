# app/db.py

import os
from dotenv   import load_dotenv
from supabase import create_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def save_message(user_id: str, role: str, content: str):
    """
    Сохраняет сообщение в таблицу messages:
    (user_id, role, content, created_at) 
    """
    supabase.table("messages").insert({
        "user_id":    user_id,
        "role":       role,
        "content":    content
    }).execute()
