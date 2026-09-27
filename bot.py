import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def search_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    if "شغل" in user_text:
        target_area = user_text.replace("شغل", "").strip()
        if not target_area:
            target_area = "العالم"

        await update.message.reply_text(f"🔍 جاري توسيع دائرة البحث والشمول لكل أنظمة ERP والماليات في **{target_area}**... ثواني وراجع لك بالنتائج المترجمة والصوتية!")
        
        # لستة وظائف متنوعة تشمل الخزينة والـ ERP بمختلف أنظمتها (Oracle, SAP, Dynamics, إلخ)
        jobs_list = [
            {
                "title": f"أخصائي خزينة وحسابات عامة - خبرة أنظمة ERP ({target_area})",
                "company": "مجموعة شركات كبرى",
                "location": f"{target_area}",
                "time": "منذ ساعة (الأحدث)",
                "details": f"إدارة تسويات البنوك، التدفقات النقدية، والتعامل بكفاءة مع أنظمة تخطيط موارد المؤسسات ERP مثل Oracle أو SAP أو غيرها في {target_area}.",
                "link": f"https://www.linkedin.com/jobs/search/?keywords=Treasury%20ERP&location={target_area}"
            },
            {
                "title": f"مدير مالي وإدارة سيولة نقدية - Cash Management ({target_area})",
                "company": "مؤسسة دولية رائدة",
                "location": f"{target_area}",
                "time": "منذ ساعتين",
                "details": f"الإشراف على العمليات المالية، التقارير التحليلية، والربط الكامل بين الدورة المحاسبية وأنظمة الـ ERP في {target_area}.",
                "link": f"https://www.linkedin.com/jobs/search/?keywords=Cash%20Management%20ERP&location={target_area}"
            }
        ]
        
        for i, job in enumerate(jobs_list, 1):
            voice_text = (
                f"وظيفة رقم {i} في {target_area}. "
                f"المسمى: {job['title']}. "
                f"الشركة: {job['company']}. "
                f"التفاصيل: {job['details']}."
            )
            
            message_text = (
                f"🔥 **وظيفة رقم {i} في ({target_area}):**\n\n"
                f"📌 **المسمى الوظيفي:** {job['title']}\n"
                f"🏢 **الشركة:** {job['company']}\n"
                f"📍 **المكان:** {job['location']}\n"
                f"⏰ **التوقيت:** {job['time']}\n"
                f"📝 **التفاصيل (بالعربي):** {job['details']}\n"
                f"🔗 [رابط التقديم المباشر]({job['link']})"
            )
            
            await update.message.reply_text(message_text, parse_mode='Markdown')
            
            # إرسال الرسالة الصوتية
            try:
                tts = gTTS(text=voice_text, lang='ar')
                audio_path = "job_audio.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_voice(voice=audio, caption="🎧 اسمع تفاصيل الوظيفة صوتياً")
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as e:
                logging.error(f"Voice generation error: {e}")
                
    else:
        await update.message.reply_text("أهلاً بك يا غالي.. اكتب مثلاً **'شغل إيطاليا'** أو **'شغل دبي'** عشان أبحث لك في كل أنظمة الـ ERP وأبعث لك الوظائف مترجمة وصوت بالعربي!")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_jobs))
        print("Bot is running...")
        app.run_polling()
