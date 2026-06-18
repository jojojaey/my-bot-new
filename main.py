from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# قاموس لحفظ طلبات المستخدمين
orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    # قائمة الاشتراكات مع تفاصيلها
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
    await query.edit_message_text("اختر الاشتراك الذي تريده:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data
    
    # تحويل الـ callback_data إلى اسم واضح
    subs_names = {
        'sub_gemini': 'Gemini Pro (سنة)',
        'sub_grok': 'SuperGrok Premium (شهر)',
        'sub_deepl': 'DeepL Pro (شهر)',
        'sub_netflix': 'Netflix 4K (شهر)',
        'sub_shahid': 'Shahid VIP (شهر)',
        'sub_crunchy': 'Crunchyroll (سنة)',
        'sub_yt': 'YouTube Premium (6 أشهر)',
        'sub_canva': 'Canva Pro (سنة)'
    }
    
    selected_sub = subs_names.get(choice, "اشتراك غير معروف")
    
    # حفظ الطلب
    orders[user.id] = f"{user.first_name} (ID: {user.id}) طلب: {selected_sub}"
    
    await query.edit_message_text(f"✅ تم تسجيل طلبك ({selected_sub}).\nسيتواصل معك الإداري قريباً!")
    print(f"طلب جديد: {orders[user.id]}")

if __name__ == '__main__':
    TOKEN ='8802340199:AAG0NEH44pFuOPeIItEms5Ea2DrkRfcnRuY'
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    
    print("Bot is running...")
    application.run_polling()
    
