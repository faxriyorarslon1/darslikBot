from django.conf import settings
from ugc.models import Profile
import telebot
from telebot import types

bot = telebot.TeleBot(settings.TOKEN)

@bot.message_handler(commands=['start','help','soat'])
def phone(message):
    if(message.text == "/start"):
        _count = Profile.objects.filter(external_id=message.from_user.id).count()
        print(_count)
        if (_count == 0):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id, "Iltimos botdan to\'liq foydalanish uchun telefon raqamingizni yuboring",
                             reply_markup=keyboard)
            
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('📣 Yangi xabarnomani qo\'shish')
            markup.row('🔕 O\'rnatilgan xabarnomani o\'chirish')

            bot.send_message(message.chat.id, "<i>Men </i>Groot<i>man 🌱</i>",
                                                reply_markup=markup, parse_mode="html")
    if(message.text == "/help"):
                         
        text = "🌱<i> Men <b>Darsliklar boti</b>man,</i>\n" \
               "<b>Men sizga darslaringiz davomida kerak bo\'ladigam ma\'lumotlarni olishingizda yordam beraman 🕙⏰</b>\n" \
               "\n🔸<i>Mendan foydalanish uchun quyidagi ketma-ketlikni amalga oshiring.</i>\n" \
               "1️⃣ O'zingizga kerak bo'lgan fanni tanlang.\n" \
               "2️⃣ Sizga yuborilgan mavzular ichidan kerakli mavzuning tartib raqamini tanlang,\n" \
               " Yuborilgan ma'lumotlardan ilm olishda foydalaning.\n\n" \
               "📌 <i>Eslatma: Bot dan to'g'ri foydalanish uchun o'qiyotgan semestr tartibingizni yuborgan bo\'lishingiz kerak!</i>"
        bot.send_message(message.chat.id,text,parse_mode='html')

    if(message.text == "/soat"):
        tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(tz)
        current_time = str(now.strftime("%H:%M"))
        bot.send_message(message.chat.id,current_time)


@bot.message_handler(content_types=['contact', 'text'])
def any_message(message):
    text = message.text
    chat_id = message.chat.id
    if (message.contact != None):
        try:
            phone_number = str(message.contact.phone_number)
            p, _ = Profile.objects.get_or_create(
                    external_id=chat_id,
                    defaults={
                    'name': message.from_user.first_name,
                    'surname':message.from_user.last_name,
                    'phone':phone_number,
                    'semestr':'1',
                    'role':'ST',
                    'faculty':'KIF'
                    }
                    )   

            bot.send_message(message.chat.id, "<i>Yo'nalish</i>ingizni tanlang:",
                                                    reply_markup=markup, parse_mode="html")
                                                    
        except Exception as e:
            bot.send_message(message.from_user.id, e)                                                    

def get_name(message):
    bot.reply_to(message, 'tamom ism olindi', parse_mode='html')

bot.infinity_polling()