import random
import asyncio
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8512510824:AAHtU250Z1BlUneRgopiC5tDtgctbBfdhkg"
CHAT_ID = "6280739103"

ist = pytz.timezone("Asia/Kolkata")

messages = [
    "🧠 Brain cooldown initiated. No phone for {x} minutes.",
    "📵 Commander order: Drop the phone for {x} minutes.",
    "⚡ Dopamine detox activated. Resume life in {x} minutes.",
    "🌿 Attention reset. Look away from screens for {x} minutes.",
    "🚨 Alert: Phone overuse detected. Lock it for {x} minutes."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Focus Break Bot Activated 🚀")

async def random_breaks(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(ist)

    if 9 <= now.hour <= 22:
        x = random.choice([10, 20, 30])
        message = random.choice(messages).format(x=x)

        await context.bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    job_queue = app.job_queue
    job_queue.run_repeating(random_breaks, interval=random.randint(600,3600), first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
