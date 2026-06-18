from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. التوكن الخاص بك
TOKEN ='8802340199:AAE66Wvg88qjA1e7scwGc8p1rfAaYH5ZnS4'

# 2. هنا ضعي الرقم الذي سيظهر لكِ بعد أن تضغطي /start
ADMIN_IDS = [000000000] 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هذا السطر سيرسل الـ ID الخاص بكِ في رسالة فورية لتعرفيه
    await update.message.reply_text(f"معرفك الخاص هو: {update.effective_user.id}")
    
    keyboard = [[InlineKeyboardButton("📦 عرض الاشتراكات", callback_data='show_subs')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك في متجرنا! اضغط الزر لعرض الاشتراكات:", reply_markup=reply_markup)

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Gemini Pro (10 د.ع - سنة)", callback_data='sub_gemini')],
        [InlineKeyboardButton("SuperGrok Premium (10 د.ع - شهر)", callback_data='sub_grok')],
        [InlineKeyboardButton("DeepL Pro (10 د.ع - شهر)", callback_data='sub_deepl')],
        [InlineKeyboardButton("Netflix 4K (10 د.ع - شهر)", callback_data='sub_netflix')],
        [InlineKeyboardButton("Shahid VIP (10 د.ع - شهر)", callback_data='sub_shahid')],
        [InlineKeyboardButton("Crunchyroll (12 د.ع - سنة)", callback_data='sub_crunchy')],
        [InlineKeyboardButton("YouTube Premium (10 د.ع - 6 أشهر)", callback_data='sub_yt')],
        [InlineKeyboardButton("Canva Pro (5 د.ع - سنة)", callback_data='sub_canva')]
    ]
    await query.edit_message_text("اختر الاشتراك المطلوب:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data
    
    # رسالة التنبيه التي ستصلك
    msg = f"🔔 طلب جديد من {user.first_name}\nالطلب: {choice}"
    
    await query.edit_message_text(f"✅ تم تسجيل طلبك ({choice}). سيتواصل معك الإداري قريباً!")
    
    # إرسال التنبيه للأرقام الموجودة في ADMIN_IDS
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=msg)
        except:
            pass

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    application.run_polling()
    
