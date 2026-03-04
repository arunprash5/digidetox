import random
import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = "8512510824:AAHtU250Z1BlUneRgopiC5tDtgctbBfdhkg"
CHAT_ID = "6280739103"

bot = Bot(token=TOKEN)

messages = [
    "🧠 Brain cooldown initiated. No phone for {x} minutes.",
    "📵 Commander order: Drop the phone for {x} minutes.",
    "⚡ Dopamine detox activated. Resume life in {x} minutes.",
    "🌿 Attention reset. Look away from screens for {x} minutes.",
    "🚨 Alert: Phone overuse detected. Lock it for {x} minutes."
]

async def send_random_break():
    while True:
        now = datetime.now()
        
        if 9 <= now.hour <= 22:
            x = random.choice([10, 20, 30])
            message = random.choice(messages).format(x=x)

            await bot.send_message(chat_id=CHAT_ID, text=message)

        wait_minutes = random.randint(10, 60)
        await asyncio.sleep(wait_minutes * 60)

asyncio.run(send_random_break())
