import random
import asyncio
from datetime import datetime, timedelta
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

# discipline tracking
obeyed = 0
ignored = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Focus Break Bot Activated 🚀\n\n"
        "I will randomly tell you to stop using your phone.\n"
        "Tap 👍 if you obey the break."
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


async def break_scheduler(app):

    bot = app.bot

    while True:

        now = datetime.now(ist)

        if 9 <= now.hour <= 22:

            # break duration
            x = random.randint(10, 20)

            end_time = now + timedelta(minutes=x)

            keyboard = [
                [
                    InlineKeyboardButton("👍 Yes", callback_data="obeyed"),
                    InlineKeyboardButton("👎 No", callback_data="ignored"),
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            message = (
                f"📵 Stop using your phone for {x} minutes.\n"
                f"Resume at {end_time.strftime('%I:%M %p')}"
            )

            await bot.send_message(
                chat_id=CHAT_ID,
                text=message + "\n\nDid you obey the break?",
                reply_markup=reply_markup,
            )

        # unpredictable next alert (30–90 minutes)
        wait_minutes = random.randint(30, 90)

        await asyncio.sleep(wait_minutes * 60)


async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CallbackQueryHandler(handle_response))

    asyncio.create_task(break_scheduler(app))

    await app.run_polling()


if __name__ == "__main__":

    asyncio.run(main())
