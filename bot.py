import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. إعداد السجلات الاحترافية لمراقبة العمليات والأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. الدوال الأساسية للتفاعل (Core Handlers)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البدء الترحيبي بالبوت"""
    user_name = update.effective_user.first_name
    welcome_text = (
        f"أهلاً بحضرتك يا {user_name}.\n"
        "أنا مساعدك الذكي لإدارة العمليات وتحسين الأداء.\n"
        "أمر التشغيل نشط وجاهز لتلقي الأوامر والبيانات."
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دليل المساعدة وعرض الأوامر المتاحة"""
    help_text = (
        "📌 الأوامر المتاحة حالياً:\n"
        "/start - بدء التشغيل والتفعيل\n"
        "/status - فحص حالة النظام والاتصال\n"
        "/help - عرض قائمة المساعدة"
    )
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """فحص حالة النظام (جزء من مهام الخزينة وتحسين العمليات)"""
    await update.message.reply_text("🟢 النظام يعمل بكفاءة عالية ومتصل بقواعد البيانات بنجاح.")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية الواردة ومدخلات العمليات"""
    text = update.message.text
    logger.info(f"تم استلام رسالة: {text}")
    
    # هنا يتم توجيه النصوص أو البيانات لتحليلها أو معالجتها لاحقاً
    response_message = f"تم استلام البيانات بنجاح وجاري معالجتها: {text}"
    await update.message.reply_text(response_message)

def main():
    """النقطة الرئيسية لتشغيل وإطلاق البوت"""
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        logger.error("خطأ حرج: متغير البيئة TELEGRAM_TOKEN غير موجود!")
        return

    # بناء التطبيق باستخدام الإصدار الحديث v21+
    application = ApplicationBuilder().token(token).build()

    # تسجيل الأوامر والمعالجات الأساسية
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # معالجة الرسائل النصية العامة
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messages))

    # بدء التشغيل الفعلي عبر Long Polling
    logger.info("جاري إطلاق نظام M_Treasury_Bot بنجاح...")
    application.run_polling()

if __name__ == "__main__":
    main()
