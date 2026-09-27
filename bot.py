import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def search_opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    if any(word in user_text for word in ["فرص", "سفر", "تدريب", "تطوع", "منحة", "منح", "دولار", "وظائف", "استشارات", "محاسبة"]):
        await update.message.reply_text("🔍 ثواني معدودة وبتكون عندك أحدث فرص السفر، التطوع، المنح، والعمل الحر بالدولار المناسبة لخبرتك.. جاهزة بالعامية!")
        
        opportunities_list = [
            {
                "title": "برنامج التطوع والتبادل الأوروبي الممولة بالكامل (European Solidarity Corps)",
                "provider": "الاتحاد الأوروبي (متاح لمصر)",
                "support": "تذاكر الطيران ذهاب وعودة + سكن كامل + تأمين صحي + مصروف جيب شهري",
                "time": "مفتوح طوال العام",
                "details": "فرصة تطوع وتدريب مهني في أوروبا وإنجلترا بتوفر لك معيشة كاملة ومغطاة 100% ومن غير شروط سن تعجيزية.",
                "link": "https://youth.europa.eu/solidarity_en"
            },
            {
                "title": "برنامج الخبراء الاستشاريين الدوليين والسفر للعمل بأوروبا وإنجلترا",
                "provider": "شبكة التوظيف والخبراء الأوروبية (EURES)",
                "support": "عقد عمل رسمي + تذاكر الطيران + السكن + راتب استشاري ممتاز",
                "time": "متاح للتقديم الآن",
                "details": "فرص سفر ووظائف بتستهدف أصحاب الخبرات الكبيرة في المحاسبة والمالية للي بيتكلموا عربي وعنجليزي.",
                "link": "https://ec.europa.eu/eures/public/en/homepage"
            },
            {
                "title": "استشاري مراجعة حسابات وأنظمة ERP عن بُعد (Senior Financial Consultant)",
                "provider": "منصات العمل الحر الدولية (Upwork)",
                "support": "أتعاب بالساعة أو بالمشروع بالدولار الأمريكي (تتحول لمصر)",
                "time": "تحديث يومي",
                "details": "شغل حر بالدولار يناسب خبرتك الكبيرة في مراجعة الحسابات وأنت قاعد في بيتك بكل مرونة ومن غير قيود سن.",
                "link": "https://www.upwork.com/freelance-jobs/accounting/"
            }
        ]
        
        for i, opp in enumerate(opportunities_list, 1):
            # النص بالعامية المصرية وبطريقة سريعة ومباشرة
            voice_text = (
                f"الفرصة رقم {i}. "
                f"المسمى: {opp['title']}. "
                f"العائد والدعم: {opp['support']}. "
                f"التفاصيل: {opp['details']}."
            )
            
            message_text = (
                f"🇪🇬 🌟 **فرصة ممولة وسفر / عمل حر رقم {i}:**\n\n"
                f"📌 **المسمى:** {opp['title']}\n"
                f"🏢 **الجهة:** {opp['provider']}\n"
                f"💰 **الدعم والسفر:** {opp['support']}\n"
                f"⏰ **التوقيت:** {opp['time']}\n"
                f"📝 **التفاصيل:** {opp['details']}\n"
                f"🔗 [رابط التقديم الرسمي والمضمون]({opp['link']})"
            )
            
            await update.message.reply_text(message_text, parse_mode='Markdown')
            
            try:
                # استخدام slow=False عشان الصوت يكون أسرع وبالعامية المصرية الواضحة
                tts = gTTS(text=voice_text, lang='ar', slow=False)
                audio_path = f"fast_opp_audio_{i}.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_voice(voice=audio, caption=f"🎧 اسمع تفاصيل الفرصة رقم {i} بالعامية السريعة")
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as e:
                logging.error(f"Voice generation error: {e}")
                
    else:
        await update.message.reply_text("يا أهلاً بيك يا محمود يا بطل.. ابعث لي كلمة زي **'فرص'**، **'سفر'**، **'تطوع'**، أو **'دولار'** وهجيب لك الخلاصة فوراً!")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_opportunities))
        print("Bot is running...")
        app.run_polling()
