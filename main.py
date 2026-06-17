from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ضع التوكين الخاص بك هنا
TOKEN ='8802340199:AAFAs9C-V2qYlIZIxnBWX-SGN4r46JnY740'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل الآن بنجاح على Railway!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    print("Bot is running...")
    application.run_polling()
    
