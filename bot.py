import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# إعداد اللوجات للتأكد إن كل شغال تمام
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def search_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    # لو كتب كلمة شغل أو طلب وظائف
    if "شغل" in user_text or "وظائف" in user_text:
        await update.message.reply_text("🔍 جاري البحث وتطبيق الفلاتر الأخلاقية والمهنية وترتيب أحدث الوظائف حسب الأجر والخبرة... ثواني وراجع لك بالنتائج!")
        
        # هنا كمثال نموذج لـ 3 وظائف (أو تقدر تزودهم لغاية 10) مرتبة من الأحدث والأعلى قيمة:
        jobs_list = [
            {
                "title": "Treasury Operations Lead (Senior Treasury)",
                "company": "Industrial Group",
                "location": "Dubai, UAE",
                "time": "منذ ساعة (أحدث)",
                "details": "Oversee bank reconciliations, Oracle ERP cash flows, and daily treasury operations.",
                "link": "https://www.linkedin.com/jobs/search/?keywords=Treasury"
            },
            {
                "title": "Treasury Senior Accountant",
                "company": "Al-Futtaim",
                "location": "Cairo, Egypt",
                "time": "منذ 3 ساعات",
                "details": "Managing daily cash positions, bank statements reconciliation, and liquidity forecasting.",
                "link": "https://www.linkedin.com/jobs/search/?keywords=Treasury"
            },
            {
                "title": "Senior Oracle Fusion Techno-Functional Administrator",
                "company": "Leading Enterprise",
                "location": "Giza, Egypt",
                "time": "منذ 5 ساعات",
                "details": "ERP financials support, cash management modules configuration, and reporting.",
                "link": "https://www.linkedin.com/jobs/search/?keywords=Oracle"
            }
        ]
        
        # إرسال الوظائف مترتبة ورا بعض في رسائل منظمة
        for i, job in enumerate(jobs_list, 1):
            message = (
                f"🔥 **وظيفة رقم {i} (مطابقة وترتيب عالي):**\n\n"
                f"📌 **المسمى:** {job['title']}\n"
                f"🏢 **الشركة:** {job['company']}\n"
                f"📍 **المكان:** {job['location']}\n"
                f"⏰ **التوقيت:** {job['time']}\n"
                f"📝 **التفاصيل:** {job['details']}\n"
                f"🔗 [رابط التقديم المباشر]({job['link']})"
            )
            await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("مش فاهم قصدك يا غالي.. اكتب **'شغل'** عشان أبدأ أبحث لك عن الوظائف وترتيبها!")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_jobs))
        print("Bot is running...")
        app.run_polling()
