import random
from datetime import datetime
import pytz

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = "8512510824:AAHtU250Z1BlUneRgopiC5tDtgctbBfdhkg"
CHAT_ID = "6280739103"

ist = pytz.timezone("Asia/Kolkata")

messages = [
    "🧠 Brain cooldown initiated. No phone for {x} minutes.",
    "📵 Commander order: Drop the phone for {x} minutes.",
    "⚡ Dopamine detox activated. Resume life in {x} minutes.",
    "🌿 Attention reset. Look away from screens for {x} minutes.",
]

# Tracking
obeyed = 0
ignored = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Focus Break Bot Activated 🚀\n\n"
        "I will randomly ask you to stop using your phone.\n"
        "Tap 👍 if you obeyed the break."
    )


async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = obeyed + ignored

    if total == 0:
        await update.message.reply_text("No breaks recorded yet.")
        return

    percent = round((obeyed / total) * 100)

    await update.message.reply_text(
        f"📊 Today's Focus Score\n\n"
        f"👍 Obeyed: {obeyed}\n"
        f"👎 Ignored: {ignored}\n"
        f"🎯 Discipline Score: {percent}%"
    )


async def random_break(context: ContextTypes.DEFAULT_TYPE):

    now = datetime.now(ist)

    if 9 <= now.hour <= 22:

        x = random.choice([10, 20, 30])

        keyboard = [
            [
                InlineKeyboardButton("👍 Yes", callback_data="obeyed"),
                InlineKeyboardButton("👎 No", callback_data="ignored"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = random.choice(messages).format(x=x)

        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message + "\n\nDid you obey the break?",
            reply_markup=reply_markup,
        )


async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global obeyed, ignored

    query = update.callback_query
    await query.answer()

    if query.data == "obeyed":
        obeyed += 1
        await query.edit_message_text("🔥 Nice discipline. Break respected.")
    else:
        ignored += 1
        await query.edit_message_text("⚠️ Break ignored. Try the next one.")


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CallbackQueryHandler(handle_response))

    job_queue = app.job_queue

    interval = random.randint(600, 3600)

    job_queue.run_repeating(random_break, interval=interval, first=10)

    app.run_polling()


if __name__ == "__main__":
    main()
