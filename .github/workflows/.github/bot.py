import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_fact():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "Ты интересный рассказчик. Придумай один короткий, увлекательный и правдоподобный факт о будущем технологий, науки или жизни людей. Пиши только на русском языке. Только сам факт, без вступлений и пояснений."
            },
            {
                "role": "user",
                "content": "Сгенерируй один интересный факт о будущем"
            }
        ],
        "temperature": 0.85,
        "max_tokens": 250
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚀 <b>Факт о будущем</b>\n\n{text}",
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()

if __name__ == "__main__":
    fact = generate_fact()
    send_to_telegram(fact)
    print("Факт успешно опубликован!")
