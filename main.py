from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN ='8802340199:AAE66Wvg88qjA1e7scwGc8p1rfAaYH5ZnS4'
# ضعي هنا الـ ID الخاص بكِ (الذي حصلتِ عليه من @userinfobot)
ADMIN_ID = [8055845627 ٫ 8959353989]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📦 عرض الاشتراكات", callback_data='show_subs')]]
    await update.message.reply_text("أهلاً بك في متجرنا! اضغط الزر لعرض الاشتراكات:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Gemini Pro (10$)", callback_data='sub_Gemini')],
        [InlineKeyboardButton("SuperGrok (10$)", callback_data='sub_Grok')],
        [InlineKeyboardButton("Canva Pro (5$)", callback_data='sub_Canva')]
    ]
    await query.edit_message_text("اختر الاشتراك المطلوب:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    choice = query.data.replace('sub_', '')
    
    # 1. إرسال إشعار للمدير (باسم العميل ورابط المحادثة معه)
    admin_text = f"🔔 **طلب اشتراك جديد**\n\n👤 العميل: {user.first_name}\n🆔 المعرف: @{user.username if user.username else 'لا يوجد'}\n📦 الطلب: {choice}"
    
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Error: {e}")

    # 2. رد للمستخدم مع زر التواصل مع المدير k7467655
    keyboard = [[InlineKeyboardButton("💬 اضغط هنا للتواصل مع المدير", url="https://t.me/k7467655")]]
    await query.edit_message_text(f"✅ تم تسجيل طلبك ({choice}).\n\nاضغط الزر أدناه للتواصل مع المدير وإتمام العملية.", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(show_subs, pattern='show_subs'))
    application.add_handler(CallbackQueryHandler(handle_choice, pattern='sub_'))
    application.run_polling()
    
