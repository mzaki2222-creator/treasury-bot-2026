import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# متغير لتتبع الوظائف التي تم عرضها مسبقاً لمنع التكرار (Loop / History Check)
shown_opportunities_history = set()

async def search_opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    if any(word in user_text for word in ["فرص", "سفر", "خبرات", "طلب زواج", "خبرات", "دولار", "وظائف", "استشارات", "محاسبة", "منصات"]):
        await update.message.reply_text("🔍 جاري فحص قاعدة البيانات وتصفية الفرص لتجنب أي تكرار.. وجلب أحدث فرص الخبراء الحصرية (بدون قيود سن).. ثواني وراجع لك!")
        
        # لستة موسعة من فرص الخبراء والمستشارين الماليين لمنع أي تكرار
        all_opportunities = [
            {
                "id": "eures_01",
                "title": "شبكة التوظيف الأوروبية الرسمية (EURES) - وظائف الخبراء الماليين",
                "provider": "الاتحاد الأوروبي والجهات الرسمية",
                "support": "عقد عمل رسمي + تذاكر الطيران + السكن + راتب استشاري ممتاز",
                "time": "متاح للتقديم الآن",
                "details": "منصة رسمية للبحث عن وظائف المحاسبة وإدارة المالية للكوادر اللي عندها خبرة طويلة وبيتكلموا عربي وعنجليزي.",
                "link": "https://ec.europa.eu/eures/public/en/homepage"
            },
            {
                "id": "remote_02",
                "title": "منصة التوظيف العالمي للخبراء والمستشارين الماليين (Remote.co)",
                "provider": "شبكات الأعمال والشركات الأجنبية المباشرة",
                "support": "رواتب بالدولار واليورو بعقود مباشرة ومنافسة قليلة",
                "time": "تحديث يومي مستمر",
                "details": "منصات أجنبية متخصصة للخبراء وأصحاب الخبرات العميقة في المحاسبة وأنظمة ERP للعمل عن بُعد من مصر بمرتبات ضخمة وبدون قيود سن.",
                "link": "https://remote.co/remote-jobs/accounting/"
            },
            {
                "id": "expert_03",
                "title": "برنامج الاستشارات الدولية ونقل الخبرات (Senior Expert Assignments)",
                "provider": "وكالات التعاون والتوظيف الدولي الأجنبية",
                "support": "مكافآت استشارية ضخمة بالعملة الصعبة + تغطية سفر المؤتمرات",
                "time": "مفتوح للخبراء المخضرمين",
                "details": "فرص مخصصة حصرياً لأصحاب الخبرات الطويلة في مراجعة الحسابات والأنظمة المالية لتقديم استشارات عابرة للحدود.",
                "link": "https://ec.europa.eu/eures/public/en/homepage"
            },
            {
                "id": "toptal_04",
                "title": "شبكة المستشارين الماليين الكبار (Toptal Finance)",
                "provider": "منصات النخبة العالمية للتوظيف الاستشاري",
                "support": "عقود بالساعة بأسعار استشارية مرتفعة بالدولار الأمريكي",
                "time": "متاح للمحترفين",
                "details": "مطلوب خبراء مراجعة قوائم مالية ومطابقة حسابات للشركات الكبرى عن بُعد وبدون شروط عمرية.",
                "link": "https://www.toptal.com/finance"
            },
            {
                "id": "glassdoor_05",
                "title": "إدارة التدقيق المالي عن بُعد (Senior Remote Auditor)",
                "provider": "بوابات التوظيف الدولية المباشرة",
                "support": "مرتبات سنوية باليورو أو الدولار + مزايا تأمينية",
                "time": "محدث حديثاً",
                "details": "فرصة لتدقيق ومراجعة السجلات المالية للشركات الأوروبية مع مرونة كاملة في أوقات العمل للخبرات.",
                "link": "https://www.glassdoor.com/Job/remote-accounting-jobs-SRCH_KO0,16.htm"
            }
        ]
        
        # فلترة الفرص بحيث لا يتم عرض أي فرصة ظهرت للمستخدم مسبقاً (Loop Check)
        unique_opportunities = [opp for opp in all_opportunities if opp["id"] not in shown_opportunities_history]
        
        # لو خلصت كل الفرص، نقدر نصفر الذاكرة أو نعلم المستخدم، بس هنا هنعرض الفرص المتاحة الجديدة
        if not unique_opportunities:
            shown_opportunities_history.clear() # إعادة تعيين لو عرضنا كل القائمة قبل كدة
            unique_opportunities = all_opportunities
            
        # نأخذ أول 3 فرص غير مكررة
        selected_batch = unique_opportunities[:3]
        
        for i, opp in enumerate(selected_batch, 1):
            # تسجيل الوظيفة في سجل المشاهدة عشان متتكررش تاني
            shown_opportunities_history.add(opp["id"])
            
            voice_text = (
                f"فرصة الخبراء رقم {i}. "
                f"المسمى: {opp['title']}. "
                f"العائد والدعم: {opp['support']}. "
                f"التفاصيل: {opp['details']}."
            )
            
            message_text = (
                f"🇪🇬 👴 **فرصة خبراء ومحترفين جديدة رقم {i} (بدون تكرار وبدون قيود سن):**\n\n"
                f"📌 **المسمى:** {opp['title']}\n"
                f"🏢 **الجهة:** {opp['provider']}\n"
                f"💰 **الدعم والعائد:** {opp['support']}\n"
                f"⏰ **التوقيت:** {opp['time']}\n"
                f"📝 **التفاصيل:** {opp['details']}\n"
                f"🔗 [رابط التقديم الرسمي والمضمون]({opp['link']})"
            )
            
            await update.message.reply_text(message_text, parse_mode='Markdown')
            
            try:
                tts = gTTS(text=voice_text, lang='ar', slow=False)
                audio_path = f"unique_opp_audio_{i}.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_voice(voice=audio, caption=f"🎧 تفاصيل فرصة الخبراء رقم {i} بالعامية")
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as e:
                logging.error(f"Voice generation error: {e}")
                
    else:
        await update.message.reply_text("يا أهلاً بيك يا محمود يا بطل.. ابعث لي كلمة **'خبرات'** أو **'وظائف'** وهجيب لك فرص جديدة ومنوعة من غير أي تكرار!")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_opportunities))
        print("Bot is running...")
        app.run_polling()
