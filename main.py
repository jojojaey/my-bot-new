from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# قاموس لحفظ طلبات المستخدمين
orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # زر "الاشتراكات" الذي يظهر في رسالة الترحيب
    keyboard = [[InlineKeyboardButton("📦 اضغط هنا لعرض الاشتراكات", callback_data='show_subs')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 أهلاً بك في بوت متجرنا.\n"
        "للاطلاع على قائمة الاشتراكات المتوفرة، اضغط على الزر بالأسفل:", 
        reply_markup=reply_markup
    )

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # قائمة الاشتراكات (يمكنك إضافة البقية بنفس الطريقة)
    keyboard = [
        [InlineKeyboardButton("Gemini Pro (10,000)", callback_data='sub_gemini')],
        [InlineKeyboardButton("Netflix 4K (10,000)", callback_data='sub_netflix')],
        [InlineKeyboardButton("Canva Pro (5,000)", callback_data='sub_canva')],
        [InlineKeyboardButton("YouTube Premium (10,000)", callback_data='sub_yt')]
    ]
    await query.edit_message_text("اختر الاشتراك الذي تريده:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data
    
    # حفظ الطلب
    orders[user.id] = f"{user.first_name} (ID: {user.id}) طلب: {choice}"
    
    await query.edit_message_text(f"✅ تم تسجيل طلبك ({choice}).\nسيتواصل معك الإداري قريباً!")
    # هذا السطر يطبع الطلب في سجلات Railway لكي تري من طلب ماذا
    print(f"طلب جديد: {orders[user.id]}")

if __name__ == '__main__':
    # ضعي التوكن الخاص بكِ هنا
    TOKEN ='8802340199:AAFAs9C-V2qYlIZIxnBWX-SGN4r46JnY740'
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    
    print("Bot is running...")
    application.run_polling()
    
