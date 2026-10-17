import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8704599199:AAFUaM81TZh5CA8d101Gs4W-hx_B6VFqERM")
CHAT_ID = os.getenv("CHAT_ID", "8364173941")

class SignalRequest(BaseModel):
    message: str

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"status": "XAUUSD Trading Bot is running successfully!"}

@app.post("/webhook")
def receive_signal(signal: SignalRequest):
    result = send_telegram_message(signal.message)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {"status": "success", "telegram_response": result}
