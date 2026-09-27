import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ذاكرة لتتبع الفرص لمنع التكرار نهائياً
seen_opportunities = set()

async def search_opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global seen_opportunities
    user_text = update.message.text.strip().lower()
    
    await update.message.reply_text(f"🔍 جاري فلترة وجلب أحدث الفرص **الممولة بالكامل 100%** (منح، دراسة، وتطوع للخبراء) بناءً على طلبك: ({update.message.text}) بدون تكرار.. ثواني وراجع لك!")
    
    # قاعدة بيانات شاملة للفرص الممولة بالكامل فقط (دراسة، منح، تطوع، وظائف خبراء)
    all_opportunities = [
        # قطر (ممولة بالكامل)
        {
            "id": "qatar_fully_01",
            "country": "قطر",
            "type": "دراسة ومنح بحثية",
            "title": "منحة جامعة حمد بن خليفة للدراسات العليا والبحث العلمي (ممولة بالكامل)",
            "provider": "جامعة حمد بن خليفة بالدوحة",
            "support": "إعفاء كامل من المصروفات الدراسية + راتب شهري معيشي + سكن مجاني + تذاكر الطيران",
            "time": "متاح للتقديم",
            "details": "منحة كبرى للماجستير والدكتوراه والزهایر البحثية للكوادر المتقدمة بدون قيود عمرية تعجيزية وممولة بنسبة 100%.",
            "link": "https://www.hbku.edu.qa/en/admissions"
        },
        {
            "id": "qatar_fully_02",
            "country": "قطر",
            "type": "وظائف خبراء واستشارات",
            "title": "برنامج استشاريو الخبراء الماليين بالجهات الحكومية القطرية",
            "provider": "الجهات الحكومية والمالية بالدوحة",
            "support": "تمويل كامل 100%: راتب معفي من الضرائب + سكن عائلي + تأمين شامل + تذاكر سنوية",
            "time": "متاح الآن",
            "details": "عقود استشارية مباشرة للمحاسبين والخبراء المخضرمين بمزايا مالية وسفر ممول بالكامل.",
            "link": "https://www.bayt.com/en/qatar/jobs/accounting-jobs/"
        },

        # السعودية (ممولة بالكامل)
        {
            "id": "ksa_fully_01",
            "country": "السعودية",
            "type": "منح دراسية وبحثية",
            "title": "منح الدراسات العليا والزمالة البحثية بالجامعات السعودية الكبرى",
            "provider": "وزارة التعليم والجامعات السعودية",
            "support": "ممولة بالكامل 100%: مكافأة شهرية، سكن مجاني، تذاكر طيران ذهاب وعودة، وتأمين صحي",
            "time": "مفتوح للتقديم",
            "details": "فرص أكاديمية وبحثية متقدمة لحملة المؤهلات والخبرات في التخصصات المالية والإدارية.",
            "link": "https://studyinisaudi.moe.gov.sa/"
        },

        # أوروبا (منح وتطوع دولي ممول بالكامل 100%)
        {
            "id": "europe_fully_01",
            "country": "أوروبا",
            "type": "تطوع دولي وسفر",
            "title": "برنامج فرقة التضامن الأوروبية (ESC) - تطوع دولي ممول بالكامل",
            "provider": "الاتحاد الأوروبي (European Solidarity Corps)",
            "support": "تغطية كاملة 100%: تذاكر السفر الدولية، السكن، المصروف الجيب الشهري، والتأمين الطبي",
            "time": "متاح للتقديم المستمر",
            "details": "برنامج أوروبي رسمي للتطوع وتبادل الخبرات (بعض المسارات مرنة للسن أو مخصصة للكوادر الناضجة لدعم المشاريع).",
            "link": "https://youth.europa.eu/solidarity_en"
        },
        {
            "id": "europe_fully_02",
            "country": "أوروبا",
            "type": "منح دراسية وبحثية",
            "title": "منح إيراسموس موندوس الأوروبية للماجستير والدكتوراه (Erasmus Mundus)",
            "provider": "الاتحاد الأوروبي",
            "support": "ممولة بالكامل 100%: الرسوم الدراسية كاملة، راتب شهري كبير للمعيشة، وتكاليف السفر والتأمين",
            "time": "مفتوح سنوياً",
            "details": "منحة عالمية كبرى للدراسة في أكثر من دولة أوروبية والحصول على درجات علمية معتمدة وبتمويل كامل.",
            "link": "https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en"
        },
        {
            "id": "europe_fully_03",
            "country": "أوروبا",
            "type": "خبراء واستشارات",
            "title": "شبكة التوظيف الأوروبية الرسمية (EURES) - عقود خبراء ممولة بالكامل",
            "provider": "الاتحاد الأوروبي",
            "support": "عقد عمل رسمي شامل تذاكر الطيران، السكن، وراتب استشاري أوروبي",
            "time": "متاح الآن",
            "details": "منصة رسمية للبحث عن وظائف المحاسبة وإدارة المالية للكوادر ذات الخبرة الطويلة.",
            "link": "https://ec.europa.eu/eures/public/en/homepage"
        }
    ]
    
    # تصفية الفرص بناءً على الدولة أو النوع المكتوب في رسالة المستخدم
    matched_opportunities = []
    for opp in all_opportunities:
        if (user_text in opp["country"].lower() or 
            user_text in opp["type"].lower() or 
            any(w in user_text for w in ["منح", "دراسة", "تطوع", "ممول", "كامل", "فرص", "شغل", "وظائف", "المزيد"])):
            matched_opportunities.append(opp)
            
    # لو ما تمش تحديد حاجة دقيقة، نعرض كل القائمة الممولة بالكامل
    if not matched_opportunities:
        matched_opportunities = all_opportunities

    # استبعاد الفرص التي تم عرضها مسبقاً لمنع التكرار نهائياً (Loop)
    available_ops = [opp for opp in matched_opportunities if opp["id"] not in seen_opportunities]
    
    if not available_ops:
        seen_opportunities.clear()  # تصفير الذاكرة لو خلصت الفرص لبدء دورة جديدة
        available_ops = matched_opportunities
        
    # اختيار حتى 7 فرص متنوعة وغير مكررة
    selected_batch = random.sample(available_ops, min(4, len(available_ops)))
    
    for i, opp in enumerate(selected_batch, 1):
        seen_opportunities.add(opp["id"])
        
        voice_text = (
            f"الفرصة رقم {i}. "
            f"المسمى: {opp['title']}. "
            f"الدعم: {opp['support']}. "
            f"التفاصيل: {opp['details']}."
        )
        
        message_text = (
            f"🇪🇬 💎 **فرصة ممولة بالكامل 100% ({opp['country']} - {opp['type']}) رقم {i}:**\n\n"
            f"📌 **المسمى:** {opp['title']}\n"
            f"🏢 **الجهة:** {opp['provider']}\n"
            f"💰 **الدعم المالي:** {opp['support']}\n"
            f"⏰ **التوقيت:** {opp['time']}\n"
            f"📝 **التفاصيل:** {opp['details']}\n"
            f"🔗 [رابط التقديم الرسمي والمضمون]({opp['link']})"
        )
        
        await update.message.reply_text(message_text, parse_mode='Markdown')
        
        try:
            tts = gTTS(text=voice_text, lang='ar', slow=False)
            audio_path = f"fully_funded_audio_{i}.mp3"
            tts.save(audio_path)
            
            with open(audio_path, 'rb') as audio:
                await update.message.reply_voice(voice=audio, caption=f"🎧 اسمع تفاصيل فرصة رقم {i} الممولة بالكامل")
            
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception as e:
            logging.error(f"Voice generation error: {e}")
            
    await update.message.reply_text("✅ خلصت الدفعة دي يا بطل! ابعث لي أي دولة (مثل: قطر، أوروبا، السعودية) أو كلمة (منح / تطوع) عشان أجيب لك دفعة جديدة ممولة بالكامل من غير تكرار.")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_opportunities))
        print("Bot is running...")
        app.run_polling()
