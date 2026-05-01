import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = ask_groq(user_text)
    await update.message.reply_text(reply)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()