from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# هنا قائمة لحفظ المستخدمين
users_list = set()

# التوكين الخاص بك
TOKEN = '8802340199:AAFAs9C-V2qY1IZIxnBWX-SGN4r46JnY740'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # إضافة المستخدم للقائمة
    users_list.add(f"{user.first_name} (ID: {user.id})")
    
    await update.message.reply_text(
        f"السلام عليك {user.first_name}، أهلاً بك في بوت اشتراك جيمني.\n"
        "يرجى الانتظار ليقوم أحد الإداريين بالتواصل معك.\n"
        "شكراً لتواصلك معنا واختيارنا!")

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إرسال قائمة الأعضاء
    if not users_list:
        await update.message.reply_text("لا يوجد أعضاء حالياً.")
    else:
        message = "قائمة الأعضاء:\n" + "\n".join(users_list)
        await update.message.reply_text(message)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # تعريف الأوامر
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('users', show_users))
    
    print("Bot is running...")
    application.run_polling()
    
