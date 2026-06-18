from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

users_list = set()
TOKEN ='8802340199:AAHCSMzIc8NB04QR8UHbQjarnOC3ia7hdAk'
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users_list.add(f"{user.first_name} (ID: {user.id})")
    await update.message.reply_text(f"السلام عليك {user.first_name}، أهلاً بك في بوت اشتراك جيمني. يرجى الانتظار ليقوم أحد الإداريين بالتواصل معك. شكراً لتواصلك معنا واختيارنا!")
async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users_list:
        await update.message.reply_text("لا يوجد أعضاء حالياً.")
    else:
        message = "قائمة الأعضاء:\n" + "\n".join(users_list)
        await update.message.reply_text(message)
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('users', show_users))
    application.run_polling()
    
