import os
import json
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# إعداد السجلات (Logging) لرصد أي أخطاء أو تناقضات فوراً
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATA_FILE = "jobs_data.json"


def load_jobs_data():
    """قراءة وتحليل بيانات الوظائف من ملف الـ JSON الخارجي مع حماية ضد الملفات التالفة"""
    if not os.path.exists(DATA_FILE):
        logger.warning(f"ملف البيانات {DATA_FILE} غير موجود!")
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        logger.error(f"خطأ في هيكل ملف الـ JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"خطأ غير متوقع أثناء قراءة ملف البيانات: {e}")
        return []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "محمود"
    welcome_message = (
        f"أهلاً بيك يا {user_name} يا بطل! 💼\n"
        "أنا نظام الخزينة والفرص الذكي (M_Treasury_Bot).\n\n"
        "🔍 **كيف تستخدم النظام؟**\n"
        "- ابعت كلمة **'شغل'** أو **'فرص'** لعرض الوظائف المتاحة.\n"
        "- ابعت اسم الدولة أو الكلمة المفتاحية للتصفية الفورية."
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    logger.info(f"استلام نص من المستخدم: {text}")

    # جلب البيانات من ملف الـ JSON
    job_listings = load_jobs_data()
    if not job_listings:
        await update.message.reply_text(
            "⚠️ **تنبيه:** ملف البيانات غير متوفر أو فارغ حالياً.",
            parse_mode="Markdown",
        )
        return

    # الفلاتر الأخلاقية والمهنية المطلوبة
    forbidden_keywords = [
        "loan",
        "loans",
        "credit facility",
        "interest",
        "قروض",
        "قرض",
        "فوائد",
        "ربا",
    ]

    matched_jobs = []
    for job in job_listings:
        full_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
        has_forbidden = any(word in full_text for word in forbidden_keywords)

        # التحقق من مطابقة النص المكتوب أو الكلمات العامة
        general_search = text in ["شغل", "/jobs", "وظائف", "فرص"]
        matches_query = general_search or (text in full_text.lower())

        if matches_query and not has_forbidden:
            matched_jobs.append(job)

    if matched_jobs:
        await update.message.reply_text(
            "🔍 جاري تطبيق الفلاتر الأخلاقية والمهنية... إليك النتائج المطابقة:"
        )
        for job in matched_jobs:
            msg = (
                f"🚨 *وظيفة Senior Treasury مطابقة!*\n\n"
                f"📌 *المسمى:* {job.get('title', 'غير محدد')}\n"
                f"🏢 *الشركة:* {job.get('company', 'غير محدد')}\n"
                f"📍 *المكان:* {job.get('location', 'غير محدد')}\n"
                f"📝 *التفاصيل:* {job.get('description', 'لا توجد تفاصيل')}\n\n"
                f"🔗 [رابط التقديم المباشر]({job.get('link', '#')})"
            )
            await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "مع الأسف مفيش وظائف مطابقة للمعايير الصارمة أو لكلمة البحث دي في الوقت الحالي، هتابع لك أول بأول!"
        )


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ سمعت رسالتك الصوتية وجاري فحص الطلب...")

    job_listings = load_jobs_data()
    if job_listings:
        job = job_listings[0]
        await update.message.reply_text(
            f"🔊 رد صوتي تجريبي: لقيت لك وظيفة مطابقة في {job.get('company')} - {job.get('location')}."
        )
    else:
        await update.message.reply_text(
            "خلصت البحث، ومفيش وظائف مطابقة حالياً يا غالي."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        f"حدث خطأ أثناء معالجة التحديث {update} بواسطة المستخدم: {context.error}"
    )


def main():
    if not TOKEN:
        logger.critical("Error: TELEGRAM_BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", handle_text))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_error_handler(error_handler)

    logger.info("M_Treasury_Bot is running and listening for commands...")
    # تشغيل البوت مع تنظيف أي تحديثات عالقة لضمان الاستجابة الفورية
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
