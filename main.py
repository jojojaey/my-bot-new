from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص ببوتك
TOKEN = '8802340199:AAE66Wvg88qjA1e7scwGc8p1rfAaYH5ZnS4'
# ضعي هنا فقط ID المدير الذي تريدينه أن يستلم الطلبات
ADMIN_IDS = [8055845627, 8959353989] 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📦 عرض الاشتراكات", callback_data='show_subs')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك في متجرنا! اضغط الزر لعرض الاشتراكات:", reply_markup=reply_markup)

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Gemini Pro (10$ - سنة)", callback_data='sub_gemini')],
        [InlineKeyboardButton("SuperGrok (10$ - شهر)", callback_data='sub_grok')],
        [InlineKeyboardButton("DeepL Pro (10$ - شهر)", callback_data='sub_deepl')],
        [InlineKeyboardButton("Netflix 4K (10$ - شهر)", callback_data='sub_netflix')],
        [InlineKeyboardButton("Shahid VIP (10$ - شهر)", callback_data='sub_shahid')],
        [InlineKeyboardButton("YouTube (10$ - 6 أشهر)", callback_data='sub_yt')],
        [InlineKeyboardButton("Canva Pro (5$ - سنة)", callback_data='sub_canva')]
    ]
    await query.edit_message_text("اختر الاشتراك المطلوب:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data
    
    # 1. تنبيه للمدير يحتوي على رابط العميل للدردشة المباشرة
    admin_msg = f"🔔 طلب اشتراك جديد!\n👤 العميل: [{user.first_name}](tg://user?id={user.id})\n📦 الطلب: {choice}"
    
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode='Markdown')
        except:
            pass
            
    # 2. زر التواصل مع المدير k7467655
    keyboard = [[InlineKeyboardButton("💬 اضغط هنا للتواصل مع المدير", url="https://t.me/k7467655")]]
    
    await query.edit_message_text(
        f"✅ تم تسجيل طلبك ({choice}).\n"
        "اضغط على الزر أدناه للتواصل مع المدير وإتمام الدفع.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    application.run_polling()
