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
                "content": "Ты опытный бизнес-аналитик и предприниматель. Придумай один короткий, практичный и интересный факт или инсайт о бизнесе, стартапах, деньгах, маркетинге, продажах, будущем предпринимательства или технологиях в бизнесе. Пиши только на русском языке. Стиль — живой, полезный, без воды и вступлений. Только сам факт или инсайт."
            },
            {
                "role": "user",
                "content": "Сгенерируй один полезный бизнес-инсайт или факт"
            }
        ],
        "temperature": 0.85,
        "max_tokens": 320
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"💼 <b>Бизнес-инсайт</b>\n\n{text}",
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()

if __name__ == "__main__":
    fact = generate_fact()
    send_to_telegram(fact)
    print("Бизнес-инсайт успешно опубликован!")
