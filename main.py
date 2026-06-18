from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بك
TOKEN ='8802340199:AAE66Wvg88qjA1e7scwGc8p1rfAaYH5ZnS4'

# ضعي هنا الـ ID الخاص بكِ والمدير الثاني (استبدلي الأصفار برقمكِ الحقيقي)
ADMIN_IDS = [8055845627, 8959353989] 

users_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users_db[user.id] = f"{user.first_name} (@{user.username})"
    
    keyboard = [[InlineKeyboardButton("📦 عرض الاشتراكات", callback_data='show_subs')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك في متجرنا! اضغط الزر لعرض الاشتراكات:", reply_markup=reply_markup)

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        msg = "👥 قائمة المستخدمين الذين دخلوا للبوت:\n\n"
        for uid, name in users_db.items():
            msg += f"👤 {name} (ID: `{uid}`)\n"
        await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("عذراً، هذا الأمر للمديرين فقط.")

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Gemini Pro (10$ - سنة)", callback_data='sub_gemini')],
        [InlineKeyboardButton("SuperGrok Premium (10$ - شهر)", callback_data='sub_grok')],
        [InlineKeyboardButton("DeepL Pro (10$ - شهر)", callback_data='sub_deepl')],
        [InlineKeyboardButton("Netflix 4K (10$ - شهر)", callback_data='sub_netflix')],
        [InlineKeyboardButton("Shahid VIP (10$ - شهر)", callback_data='sub_shahid')],
        [InlineKeyboardButton("Crunchyroll (12$ - سنة)", callback_data='sub_crunchy')],
        [InlineKeyboardButton("YouTube Premium (10$ - 6 أشهر)", callback_data='sub_yt')],
        [InlineKeyboardButton("Canva Pro (5$ - سنة)", callback_data='sub_canva')]
    ]
    await query.edit_message_text("اختر الاشتراك المطلوب:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data
    
    # رسالة للمدير مع رابط مباشر للدردشة مع المستخدم
    msg = f"🔔 طلب جديد من: [{user.first_name}](tg://user?id={user.id})\n🆔 الـ ID: `{user.id}`\n📦 الطلب: {choice}"
    
    # رد للعميل مع زر التواصل مع المدير
    keyboard = [[InlineKeyboardButton("💬 اضغط هنا للتواصل مع المدير", url="https://t.me/k7467655")]]
    
    await query.edit_message_text(
        f"✅ تم تسجيل طلبك ({choice}).\n"
        "اضغط على الزر أدناه للتواصل مع المدير وإتمام الدفع.\n"
        "شكراً لاختيارنا! 🌹",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # إرسال التنبيه للمديرين
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=msg, parse_mode='Markdown')
        except:
            pass

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('users', show_users))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    application.run_polling()
    
