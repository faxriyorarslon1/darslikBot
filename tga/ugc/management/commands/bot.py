from django.conf import settings
from ugc.models import Profile, Faculty, Area, Subjects, Lectures, Laboratories
import telebot
from telebot import types

bot = telebot.TeleBot(settings.TOKEN)

def get_link(link, chat_id):
    link = link.split('/')
    username = f"@{link[3]}"
    bot.forward_message(chat_id, username, int(link[4]))
    

def del_mes(message):
    try:
        bot.delete_message(message.chat.id, (message.id-4))
    except Exception as e:
        print(e)
        

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
            u_id = message.from_user.id
            chat_id=message.chat.id
            data = Profile.objects.filter(external_id = u_id).get()
            subjects = Subjects.objects.filter(semestr = data.semestr).filter(area = data.area).all()
            markup = types.InlineKeyboardMarkup()
            for subject in subjects:
                item = types.InlineKeyboardButton(subject.name, callback_data=f"#{subject.name}")
                markup.add(item)
            bot.send_message(message.chat.id,"Sizda quyidagi fanlar mavjud:", reply_markup=markup)
    if(message.text == "/help"):
                         
        text = "🌱<i> Men <b>Darsliklar boti</b>man,</i>\n" \
               "<b>Men sizga darslaringiz davomida kerak bo\'ladigam ma\'lumotlarni olishingizda yordam beraman 🕙⏰</b>\n" \
               "\n🔸<i>Mendan foydalanish uchun quyidagi ketma-ketlikni amalga oshiring.</i>\n" \
               "1️⃣ O'zingizga kerak bo'lgan fanni tanlang.\n" \
               "2️⃣ Sizga yuborilgan mavzular ichidan kerakli mavzuning tartib raqamini tanlang,\n" \
               " Yuborilgan ma'lumotlardan ilm olishda foydalaning.\n\n" \
               "📌 <i>Eslatma: Bot dan to'g'ri foydalanish uchun o'qiyotgan semestr tartibingizni yuborgan bo\'lishingiz kerak!</i>"
        bot.send_message(message.chat.id,text,parse_mode='html')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data[0] == "#":
        subject_name = call.data[1:]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Ma'ruza", "Laboratoriya")
        bot.answer_callback_query(call.id, "O'zingizga kerak bo'limni tanlang")    
        bot.send_message(call.message.chat.id, "O'zingizga kerak bo'limni tanlang", reply_markup=markup)
        bot.register_next_step_handler(call.message, choose, subject_name)
    elif call.data[0] == "*":
        data = call.data.split('@')
        theme_number = int(data[0][1:])
        subject_name = data[1]
        subject = Subjects.objects.filter(name = subject_name).get()
        laboratories = Laboratories.objects.filter(subject=subject).all()
        i = 1
        for laboratorie in laboratories:
            if theme_number == i:
                get_link(laboratorie.ppt_file, chat_id)
                get_link(laboratorie.word_file, chat_id)
                get_link(laboratorie.video, chat_id)
                break
        bot.answer_callback_query(call.id, "Bizda quyidagi ma'lumotlar bor")        

    elif call.data[0] == "-":
        data = call.data.split('@')
        theme_number = int(data[0][1:])
        subject_name = data[1]
        subject = Subjects.objects.filter(name = subject_name).get()
        lectures = Lectures.objects.filter(subject=subject).all()
        i = 1
        for lecture in lectures:
            if theme_number == i:
                get_link(lecture.ppt_file, chat_id)
                get_link(lecture.word_file, chat_id)
                get_link(lecture.video, chat_id)
                get_link(lecture.other_file, chat_id)
                break
        bot.answer_callback_query(call.id, "Bizda quyidagi ma'lumotlar bor")

@bot.message_handler(content_types=['contact', 'text'])
def any_message(message):
    text = message.text
    chat_id = message.from_user.id
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
                    'faculty':Faculty.objects.filter(id=1).get(),
                    'area':Area.objects.filter(id=1).get(),
                    }
                    )  

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for faculty in Faculty.objects.all():
                markup.row(faculty.name)

            bot.send_message(message.chat.id, "<i>Fakultet</i>ingizni tanlang:", parse_mode="html", reply_markup = markup)
            bot.register_next_step_handler(message, set_faculty)
                                                    
        except Exception as e:
            bot.send_message(message.from_user.id, e)                                                    

def set_faculty(message):
    u_id = message.from_user.id
    faculty_name=Faculty.objects.filter(name=message.text).get()
    if faculty_name:
        Profile.objects.filter(external_id=u_id).update(faculty=faculty_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for area in Area.objects.filter(faculty = faculty_name).all():
                markup.row(area.name)
        bot.send_message(message.chat.id, "<i>Yo'nalish</i>ingizni tanlang:", parse_mode="html", reply_markup = markup)
        bot.register_next_step_handler(message, set_area)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for faculty in Faculty.objects.all():
            markup.row(faculty.name)

        bot.send_message(message.chat.id, "Siz noto'g'ri ko'rinishdagi javob yubordingiz.\nIltimos<i>Fakultet</i>ingizni tanlang:", parse_mode="html", reply_markup = markup)
        bot.register_next_step_handler(message, set_faculty)


def set_area(message):
    u_id = message.from_user.id
    area_name=Area.objects.filter(name=message.text).get()
    if area_name:
        Profile.objects.filter(external_id=u_id).update(area=area_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("1","2","3")
        markup.row("4","5","6")
        markup.row("7","8")
    
        bot.send_message(message.chat.id, "<i>O'qiyotgan semestr</i>ingizni tanlang:", parse_mode="html", reply_markup = markup)
        bot.register_next_step_handler(message, set_semestr)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for faculty in Faculty.objects.all():
            markup.row(faculty.name)

        bot.send_message(message.chat.id, "Siz noto'g'ri ko'rinishdagi javob yubordingiz.\nIltimos<i>Yo'nalish</i>ingizni tanlang:", parse_mode="html", reply_markup = markup)
        bot.register_next_step_handler(message, set_area)


def set_semestr(message):
    u_id = message.from_user.id
    semestr_number = message.text
    if int(semestr_number) > 0 and int(semestr_number) < 9:
        del_mes(message)
        Profile.objects.filter(external_id=u_id).update(semestr = semestr_number)
        text = "Tabriklaymiz siz <b>muvaffaqiyatli</b> tarzda ro'yxatdan o'tdingiz."\
        "\nEndi botimiz qulayliklaridan foydalanishingiz mumkin."
        bot.send_message(u_id, text, parse_mode='html')

        u_id = message.from_user.id
        chat_id=message.chat.id
        data = Profile.objects.filter(external_id = u_id).get()
        subjects = Subjects.objects.filter(semestr = data.semestr).filter(area = data.area).all()
        markup = types.InlineKeyboardMarkup()
        for subject in subjects:
            item = types.InlineKeyboardButton(subject.name, callback_data=f"#{subject.name}")
            markup.add(item)
        bot.send_message(u_id,"Sizda quyidagi fanlar mavjud:", reply_markup=markup)
        
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("1","2","3")
        markup.row("4","5","6")
        markup.row("7","8")
        bot.send_message(message.chat.id, "<i>O'qiyotgan semestr</i>xato kiritdingiz.Iltimos qaytadan tanlang:", parse_mode="html", reply_markup = markup)
        bot.register_next_step_handler(message, set_semestr)


def choose(message, subject_name):
    del_mes(message)
    subject = Subjects.objects.filter(name = subject_name).get()
    m_text = message.text
    u_id = message.from_user.id
    user = Profile.objects.filter(external_id=u_id).get()

    if m_text == "Ma'ruza":
        lectures = Lectures.objects.filter(subject=subject).all()
        
        number = 1
        inline = types.InlineKeyboardMarkup()
        for lecture in lectures:
            item = types.InlineKeyboardButton(number, callback_data=f"-{number}@{subject.name}")
            inline.add(item)
            number+=1
        
        get_link(subject.themes_list, u_id)
        bot.send_message(u_id, "Kerakli mavzuni tartib raqamini tanlang!", reply_markup=inline)            
        
    elif m_text == "Laboratoriya":
        laboratories = Laboratories.objects.filter(subject=subject).all()
        number = 1
        inline = types.InlineKeyboardMarkup()
        for laboratorie in laboratories:
            item = types.InlineKeyboardButton(number, callback_data=f"*{number}@{subject.name}")
            inline.add(item)
            number+=1
        
        get_link(subject.themes_list, u_id)
        bot.send_message(u_id, "Kerakli mavzuni tartib raqamini tanlang!", reply_markup=inline)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        del_mes(message)
        markup.row("Ma'ruza", "Laboratoriya")
        bot.send_message(u_id, "<b>Siz aniqlanmagan turdagi javob qaytardingiz</b>\nIltimos O'zingizga kerak bo'limni tanlang!", reply_markup=markup, parse_mode='html')
        bot.register_next_step_handler(message, choose)   





bot.infinity_polling()