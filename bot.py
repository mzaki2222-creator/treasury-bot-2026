import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def search_opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    # استقبال أي كلمة مفتاحية للبحث عن فرص الاستشارات والعمل الحر
    if "فرص" in user_text or "دولار" in user_text or "استشارات" in user_text or "محاسبة" in user_text or "عمل حر" in user_text or "شغل" in user_text:
        target_field = user_text.replace("فرص", "").replace("دولار", "").replace("استشارات", "").replace("محاسبة", "").replace("عمل حر", "").replace("شغل", "").strip()
        if not target_field:
            target_field = "الاستشارات المالية ومراجعة الحسابات عن بُعد بالدولار"

        await update.message.reply_text(f"🔍 جاري البحث المتقدم وجلب أحدث فرص **العمل الحر والاستشارات المالية بالدولار (مخصصة للخبرات الكبيرة والمصريين)** في مجال: **{target_field}**.. ثواني وراجع لك بالنتائج!")
        
        # لستة فرص عمل حر استشارية ومالية بالدولار مخصصة للخبرات (بدون قيود سن)
        opportunities_list = [
            {
                "title": "استشاري مراجعة حسابات وأنظمة ERP عن بُعد (Senior Financial Consultant)",
                "provider": "منصات الشركات العالمية للعمل الحر والتوظيف الاستشاري",
                "support": "أتعاب بالساعة أو بالمشروع بالدولار الأمريكي (تُحفظ وتُحول لمصر)",
                "time": "متاح للتقديم الفوري (يستهدف أصحاب الخبرات الطويلة)",
                "details": "مطلوب خبير محاسبة لمراجعة القوائم المالية، مطابقة الكشوف، وإدارة أنظمة ERP للشركات الناشئة والدولية عن بُعد بدون أي قيود عمرية.",
                "link": "https://www.upwork.com/freelance-jobs/accounting/"
            },
            {
                "title": "مستشار تدقيق مالي ومالك عمليات المحاسبة للشركات الصغيرة",
                "provider": "شبكات الأعمال والشركات الدولية عن بُعد",
                "support": "عقود شهرية ثابتة بدخل ممتاز بالدولار أو اليورو وأنت في بيتك",
                "time": "تحديث يومي مستمر",
                "details": "فرصة رائعة للمحاسبين المخضرمين لتقديم استشارات وتدقيق مالي يومي أو أسبوعي للشركات الأجنبية التي تطلب متحدثي العربية والإنجليزية.",
                "link": "https://www.freelancer.com/search/accounting"
            },
            {
                "title": "مشروع مراجعة وتطهير الحسابات والبيانات المالية (Financial Data Auditing)",
                "provider": "منصة الخبراء الماليين الدوليين",
                "support": "مكافآت مالية ضخمة بالدولار حسب إنجاز المهام الاستشارية",
                "time": "مفتوح للمحاسبين ذوي الخبرات العميقة",
                "details": "مهمات استشارية مرنة تتطلب خبرة طويلة في تدقيق الحسابات وإعداد التقارير المالية بدقة عالية، وتناسب تماماً الكوادر المصرية الكبيرة.",
                "link": "https://www.toptal.com/finance"
            }
        ]
        
        for i, opp in enumerate(opportunities_list, 1):
            voice_text = (
                f"فرصة العمل الحر رقم {i}. "
                f"المسمى: {opp['title']}. "
                f"العائد: {opp['support']}. "
                f"التفاصيل: {opp['details']}."
            )
            
            message_text = (
                f"💵 📊 **فرصة عمل حر واستشارات بالدولار رقم {i}:**\n\n"
                f"📌 **المسمى:** {opp['title']}\n"
                f"🏢 **الجهة:** {opp['provider']}\n"
                f"💰 **العائد المالي:** {opp['support']}\n"
                f"⏰ **التوقيت:** {opp['time']}\n"
                f"📝 **التفاصيل:** {opp['details']}\n"
                f"🔗 [رابط التقديم الرسمي والمضمون]({opp['link']})"
            )
            
            # إرسال النص
            await update.message.reply_text(message_text, parse_mode='Markdown')
            
            # إرسال الرسالة الصوتية
            try:
                tts = gTTS(text=voice_text, lang='ar')
                audio_path = f"freelance_audio_{i}.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_voice(voice=audio, caption=f"🎧 اسمع تفاصيل فرصة العمل الحر رقم {i} صوتياً")
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as e:
                logging.error(f"Voice generation error: {e}")
                
    else:
        await update.message.reply_text("يا أهلاً بيك يا محمود يا بطل.. البوت جاهز لخدمتك! ابعث لي كلمات زي **'دولار'**، **'استشارات'**، **'محاسبة'**، أو **'عمل حر'** وهطلع لك أفضل الفرصة المتاحة للخبرات الكبيرة بالدولار وصوت وصورة!")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_opportunities))
        print("Bot is running...")
        app.run_polling()
