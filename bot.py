import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص ببوتك (سيتم قراءته بأمان من إعدادات Render)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# قاعدة بيانات تجريبية لوظائف الـ Senior Treasury
job_listings = [
    {
        "title": "Senior Treasury Manager",
        "company": "Multinational FMCG",
        "location": "Cairo, Egypt",
        "description": "Manage cash flow, liquidity, and working capital without conventional interest or loans.",
        "link": "https://linkedin.com/jobs/sample1"
    },
    {
        "title": "Treasury Operations Lead",
        "company": "Industrial Group",
        "location": "Dubai, UAE",
        "description": "Oversee bank reconciliations, Oracle ERP cash flows, and daily treasury operations.",
        "link": "https://linkedin.com/jobs/sample3"
    }
]

# الفلاتر الأخلاقية والمهنية
forbidden_keywords = ["loan", "loans", "credit facility", "interest", "قروض", "قرض", "فوائد", "ربا"]
allowed_keywords = ["treasury", "cash management", "liquidity", "working capital", "bank reconciliation", "خزينة"]

def filter_jobs():
    matched = []
    for job in job_listings:
        full_text = (job['title'] + " " + job['description']).lower()
        has_forbidden = any(word in full_text for word in forbidden_keywords)
        is_allowed = any(word in full_text for word in allowed_keywords)
        
        if is_allowed and not has_forbidden:
            matched.append(job)
    return matched

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بيك يا محمود يا بطل! 💼\n"
        "أنا بوت الخزينة الذكي (`M_Treasury_Bot`).\n"
        "اكتب كلمة **'شغل'** أو ابعت لي فويس نوت عشان أبحث لك عن أحدث وظائف الـ Senior Treasury النظيفة والمناسبة ليك."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    
    if text in ["شغل", "/jobs", "وظائف"]:
        await update.message.reply_text("🔍 جاري البحث وتطبيق الفلاتر الأخلاقية والمهنية... ثواني وراجع لك بالنتائج!")
        
        matched_jobs = filter_jobs()
        if matched_jobs:
            for job in matched_jobs:
                msg = (
                    f"🚨 *وظيفة Senior Treasury مطابقة!*\n\n"
                    f"📌 *المسمى:* {job['title']}\n"
                    f"🏢 *الشركة:* {job['company']}\n"
                    f"📍 *المكان:* {job['location']}\n"
                    f"📝 *التفاصيل:* {job['description']}\n\n"
                    f"🔗 [رابط التقديم]({job['link']})"
                )
                await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("مع الأسف مفيش وظائف مطابقة للمعايير الصارمة دي في الوقت الحالي، هتابع لك أول بأول!")
    else:
        await update.message.reply_text("مش فاهم قصدك يا غالي.. اكتب **'شغل'** عشان أبدأ أبحث لك عن الوظائف!")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # استقبال الرسالة الصوتية وتأكيد التفاعل
    await update.message.reply_text("🎙️ سمعت رسالتك الصوتية وجاري فحص الطلب...")
    
    matched_jobs = filter_jobs()
    if matched_jobs:
        job = matched_jobs[0]
        await update.message.reply_text(f"🔊 رد صوتي تجريبي: لقيت لك وظيفة مطابقة في {job['company']} - {job['location']}.")
    else:
        await update.message.reply_text("خلصت البحث، ومفيش وظائف مطابقة حالياً يا غالي.")

def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", handle_text))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    print("M_Treasury_Bot is running and listening for commands...")
    app.run_polling()

if __name__ == "__main__":
    main()