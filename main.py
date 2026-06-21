from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8802340199:AAE66Wvg88qjA1e7scwGc8p1rfAaYH5ZnS4'
ADMIN_IDS = [8055845627, 8959353989] 
CHANNEL_USERNAME = "@MONEYMODE1825"

SUBS = [
    ("Gemini Pro (10$ - سنة)", "sub_gemini"),
    ("SuperGrok Premium (10$ - شهر)", "sub_grok"),
    ("DeepL Pro (10$ - شهر)", "sub_deepl"),
    ("Netflix 4K (10$ - شهر)", "sub_netflix"),
    ("Shahid VIP (10$ - شهر)", "sub_shahid"),
    ("Crunchyroll (12$ - سنة)", "sub_crunchy"),
    ("YouTube Premium (10$ - 6 أشهر)", "sub_yt"),
    ("Canva Pro (5$ - سنة)", "sub_canva")
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة أولاً", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("✅ تم الاشتراك، عرض العروض", callback_data='show_subs')]
    ]
    await update.message.reply_text("أهلاً بك! يرجى الاشتراك في القناة للوصول للعروض:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in SUBS]
    await query.edit_message_text("اختر الاشتراك المطلوب:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data
    
    # تحويل اسم العميل إلى رابط مباشر (tg://user?id=...)
    # هذا يخليكِ بمجرد الضغط على الاسم تفتحين محادثة الشخص
    customer_link = f"[{user.full_name}](tg://user?id={user.id})"
    username = f"@{user.username}" if user.username else "لا يوجد يوزر"
    
    choice_text = next((text for text, data in SUBS if data == choice), choice)
    
    # الإشعار المحدث: الاسم الآن عبارة عن رابط للمحادثة
    msg = (f"🔔 طلب اشتراك جديد!\n\n"
           f"👤 العميل: {customer_link}\n"
           f"🆔 اليوزر: {username}\n"
           f"🔢 الآيدي: `{user.id}`\n"
           f"📦 الطلب: {choice_text}")
    
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode='Markdown')
        except: pass
            
    keyboard = [[InlineKeyboardButton("💬 اضغط هنا للتواصل مع المدير", url="https://t.me/k7467655")]]
    await query.edit_message_text(
        f"✅ تم تسجيل طلبك ({choice_text}).\n"
        "شكراً لاختيارنا! 🌹", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    application.run_polling()
    
