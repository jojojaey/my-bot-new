from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN ='8802340199:AAE66Wvg88qjA1e7scwGc8p1rfAaYH5ZnS4'
ADMIN_IDS = [8055845627, 8959353989] 
CHANNEL_ID = "@MONEYMODE1825" # ضعي معرف قناتك هنا (مثلاً @Katri_V)

# قاموس اللغات
LANGS = {
    'ar': {'start': "مرحباً! اختر لغتك:", 'join': "اشترك في القناة أولاً:", 'check': "تم الانضمام", 'subs': "عرض الاشتراكات", 'choice': "اختر اشتراكك:", 'contact': "💬 تواصل مع المدير"},
    'en': {'start': "Welcome! Choose your language:", 'join': "Join the channel first:", 'check': "I joined", 'subs': "Show Subscriptions", 'choice': "Choose your sub:", 'contact': "💬 Contact Manager"}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("العربية 🇦🇷", callback_data='lang_ar'), InlineKeyboardButton("English 🇺🇸", callback_data='lang_en')]]
    await update.message.reply_text("Welcome! Choose your language / أهلاً بك، اختر لغتك:", reply_markup=InlineKeyboardMarkup(keyboard))

async def lang_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    keyboard = [[InlineKeyboardButton("🔗 اضغط هنا للاشتراك", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                [InlineKeyboardButton(LANGS[lang]['check'], callback_data='check_sub')]]
    await query.edit_message_text(LANGS[lang]['join'], reply_markup=InlineKeyboardMarkup(keyboard))

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = context.user_data.get('lang', 'ar')
    # ملاحظة: التحقق البرمجي الكامل يحتاج صلاحيات البوت في القناة
    keyboard = [[InlineKeyboardButton(LANGS[lang]['subs'], callback_data='show_subs')]]
    await query.edit_message_text(LANGS[lang]['choice'], reply_markup=InlineKeyboardMarkup(keyboard))

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = context.user_data.get('lang', 'ar')
    keyboard = [[InlineKeyboardButton("Gemini Pro (10$)", callback_data='sub_gemini')], [InlineKeyboardButton(LANGS[lang]['contact'], url="https://t.me/k7467655")]]
    await query.edit_message_text(LANGS[lang]['choice'], reply_markup=InlineKeyboardMarkup(keyboard))

# دالة handle_choice تبقى كما هي لإرسال الإشعار للمدير

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(lang_select, pattern='lang_'))
    application.add_handler(CallbackQueryHandler(check_sub, pattern='check_sub'))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.run_polling()
    
