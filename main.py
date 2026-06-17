import os
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = '8802340199:AAFAs9C-V2qYlIZlxnBWX-SGN4r46JnY740'

async def start(update, context):
    await update.message.reply_text("Hello! The bot is working on Railway.")

if __name__ == '__main__':
    # استخدام الـ Port الذي يوفره Railway
    port = int(os.environ.get("PORT", 8080))
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # تشغيل البوت
    print("Bot is starting...")
    app.run_polling()
    
