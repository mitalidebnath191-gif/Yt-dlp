import os
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("8924348360:AAFA5IaNEbiaemwDZDPb3Zfvo2uIwSDHKPg")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text.startswith("@yt "):
        return

    query = text[4:].strip()

    try:
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "skip_download": True
        }

        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch5:{query}",
                download=False
            )

        if not result.get("entries"):
            await update.message.reply_text("কোনো ভিডিও পাওয়া যায়নি।")
            return

        msg = f"🔍 Result for: {query}\n\n"

        for i, video in enumerate(result["entries"], start=1):
            title = video.get("title", "Unknown")
            vid = video.get("id", "")
            url = f"https://www.youtube.com/watch?v={vid}"

            msg += f"{i}. {title}\n{url}\n\n"

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
