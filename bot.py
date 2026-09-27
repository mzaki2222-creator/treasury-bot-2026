import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def search_opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    if any(word in user_text for word in ["فرص", "سفر", "تدريب", "تطوع", "منحة", "منح", "دولار", "وظائف", "استشارات", "محاسبة", "منصات"]):
        await update.message.reply_text("🔍 ثواني وبتكون عندك أحدث فرص المنح، السفر، والتوظيف المباشر في المنصات الأجنبية (بعيداً عن زحمة أب وورك).. جاهزة بالعامية!")
        
        # قائمة البدائل الأجنبية المباشرة ومواقع التوظيف والمنح للخبراء والمصريين
        opportunities_list = [
            {
                "title": "منح الدراسات العليا والتبادل المهني الممولة بالكامل (Stipend)",
                "provider": "برامج الاتحاد الأوروبي والمنح الدولية",
                "support": "تذاكر الطيران + السكن + تأمين صحي + مصروف جيب شهري مغطى بالكامل",
                "time": "مفتوح للتقديم للمصريين",
                "details": "منح دراسية ومهنية في أوروبا وإنجلترا بتوفر معيشة متكاملة براتب وبدون شروط سن تعجيزية.",
                "link": "https://youth.europa.eu/solidarity_en"
            },
            {
                "title": "شبكة التوظيف الأوروبية الرسمية (EURES) - فرص سفر وعمل للخبراء",
                "provider": "الاتحاد الأوروبي والجهات الرسمية",
                "support": "عقد عمل رسمي + تذاكر الطيران + السكن + راتب استشاري ممتاز",
                "time": "متاح للتقديم الآن",
                "details": "منصة أوروبية رسمية ومباشرة للبحث عن وظائف المحاسبة وإدارة المالية للكوادر المصرية اللي بيتكلموا عربي وعنجليزي.",
                "link": "https://ec.europa.eu/eures/public/en/homepage"
            },
            {
                "title": "منصة التوظيف العالمي للخبراء والمستشارين الماليين (Toptal & Remote.co)",
                "provider": "شبكات الأعمال والشركات الأجنبية المباشرة",
                "support": "رواتب بالدولار واليورو بعقود مباشرة بدون منافسة عشوائية",
                "time": "تحديث يومي مستمر",
                "details": "منصات أجنبية متخصصة للخبراء وأصحاب الخبرات العميقة في المحاسبة وأنظمة ERP للعمل عن بُعد من مصر بمرتبات ضخمة.",
                "link": "https://remote.co/remote-jobs/accounting/"
            }
        ]
        
        for i, opp in enumerate(opportunities_list, 1):
            voice_text = (
                f"الفرصة رقم {i}. "
                f"المسمى: {opp['title']}. "
                f"الدعم أو العائد: {opp['support']}. "
                f"التفاصيل: {opp['details']}."
            )
            
            message_text = (
                f"🇪🇬 🌟 **فرصة منصات أجنبية / سفر / منح رقم {i}:**\n\n"
                f"📌 **المسمى:** {opp['title']}\n"
                f"🏢 **الجهة:** {opp['provider']}\n"
                f"💰 **الدعم والسفر:** {opp['support']}\n"
                f"⏰ **التوقيت:** {opp['time']}\n"
                f"📝 **التفاصيل:** {opp['details']}\n"
                f"🔗 [رابط التقديم الرسمي والمضمون]({opp['link']})"
            )
            
            await update.message.reply_text(message_text, parse_mode='Markdown')
            
            try:
                tts = gTTS(text=voice_text, lang='ar', slow=False)
                audio_path = f"direct_opp_audio_{i}.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_voice(voice=audio, caption=f"🎧 اسمع تفاصيل الفرصة رقم {i} بالعامية السريعة")
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as e:
                logging.error(f"Voice generation error: {e}")
                
    else:
        await update.message.reply_text("يا أهلاً بيك يا محمود يا بطل.. ابعث لي كلمة زي **'منصات'**، **'سفر'**، **'منح'**، أو **'وظائف'** وهجيب لك الخلاصة في المنصات الأجنبية فوراً!")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_opportunities))
        print("Bot is running...")
        app.run_polling()
