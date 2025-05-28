# main.py

from fastapi import FastAPI, Request
from app.handlers import handle_update

app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    result = await handle_update(data)
    # возвращаем словарь {"chat_id":..., "text":...}
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
