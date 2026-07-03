# -*- coding: utf-8 -*-
import telebot
import re
import time

TOKEN = "8670803464:AAE-DBwo7Nl8YoNGbDP6YPt_aUqaWdQLzqU"

bot = telebot.TeleBot(TOKEN)

# ===== УДАЛЯЕМ WEBHOOK =====
try:
    bot.remove_webhook()
    print("✅ Webhook удалён")
except Exception as e:
    print(f"⚠️ Ошибка удаления webhook: {e}")

# ===== ID КАНАЛА И ГРУППЫ =====
CHANNEL_ID = -1002120670742  # ID КАНАЛА (бот НЕ админ!)
DISCUSSION_GROUP_ID = -1002054714983  # ID ГРУППЫ ОБСУЖДЕНИЯ (бот АДМИН!)

# ===== ПРАВИЛА =====
RULES = """📢 **ПРАВИЛА КОММЕНТАРИЕВ**

🚫 **ЗАПРЕЩЕНО:**
1️⃣ Спам, реклама, ссылки
2️⃣ Материалы 18+
3️⃣ Оскорбления, унижения
4️⃣ Угрозы и агрессия
5️⃣ Дискриминация, расизм, экстремизм
6️⃣ Сексуальные домогательства
7️⃣ Твич-запретки

⚠️ Нарушение = удаление комментария."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот запущен!")

@bot.message_handler(commands=['rules'])
def send_rules(message):
    bot.reply_to(message, RULES)

@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"🆔 ID: `{message.chat.id}`")

# =====================================================
# ФУНКЦИИ ДЕТЕКТА
# =====================================================

def clean_text(text):
    text = re.sub(r'[^a-zA-Zа-яА-Я]', '', text)
    return text.lower()

def is_similar(word1, word2, threshold=0.7):
    if len(word1) < 3 or len(word2) < 3:
        return False
    matches = sum(1 for a, b in zip(word1, word2) if a == b)
    ratio = matches / max(len(word1), len(word2))
    return ratio >= threshold

# ============================================
# БАЗА ЗАПРЕТОВ
# ============================================

THREATS = [
    ("угроза", ["убью", "yбью", "убъю", "убйу"]),
    ("угроза", ["зарежу", "зaрежу", "зарежy"]),
    ("угроза", ["убей", "yбей", "убеи"]),
    ("угроза", ["сдохни", "сдoxни", "сдox"]),
    ("угроза", ["умри", "yмри", "умрu"]),
    ("угроза", ["завалю", "зaвалю"]),
    ("угроза", ["порву", "пoрву"]),
    ("угроза", ["разорву", "рaзорву"]),
    ("угроза", ["кончу", "кoнчу"]),
    ("угроза", ["могила", "мoгила"]),
    ("угроза", ["труп", "трyп"]),
    ("угроза", ["убийца", "yбийца"]),
    ("угроза", ["киллер", "кuллер"]),
    ("угроза", ["застрелю", "застрел"]),
    ("угроза", ["закопаю", "закoпаю"]),
    ("угроза", ["прикончу", "прикoнчу"]),
    ("угроза", ["грохну", "грoxну"]),
    ("угроза", ["смерть", "смepть"]),
]

INSULTS = [
    ("оскорбление", ["тупой", "тyпой"]),
    ("оскорбление", ["тупица", "тyпица"]),
    ("оскорбление", ["дебил", "дeбил"]),
    ("оскорбление", ["идиот", "uдиот"]),
    ("оскорбление", ["кретин", "крeтин"]),
    ("оскорбление", ["дурак", "дyрак"]),
    ("оскорбление", ["глупый", "глyпый"]),
    ("оскорбление", ["бездарь", "бeздарь"]),
    ("оскорбление", ["урод", "yрод"]),
    ("оскорбление", ["чмо", "чмo"]),
    ("оскорбление", ["лох", "лox"]),
    ("оскорбление", ["дегенерат", "дeгенерат"]),
    ("оскорбление", ["имбецил", "uмбецил"]),
    ("оскорбление", ["олень", "oлень"]),
    ("оскорбление", ["баран", "бaран"]),
    ("оскорбление", ["козел", "кoзел"]),
    ("оскорбление", ["свинья", "cвинья"]),
    ("оскорбление", ["собака", "cобака"]),
    ("оскорбление", ["крыса", "кpыса"]),
    ("оскорбление", ["паразит", "пapaзит"]),
]

DISCRIMINATION = [
    ("дискриминация", ["нацист", "нaцист"]),
    ("дискриминация", ["фашист", "фaшист"]),
    ("дискриминация", ["расист", "рaсист"]),
    ("дискриминация", ["скинхед", "скuнхед"]),
    ("дискриминация", ["хохол", "xoxол"]),
    ("дискриминация", ["жид", "жuд"]),
    ("дискриминация", ["чурка", "чypка"]),
    ("дискриминация", ["совок", "cовок"]),
    ("дискриминация", ["ватник", "вaтник"]),
]

SEXUAL = [
    ("сексуальное домогательство", ["изнасилование", "изнacилование"]),
    ("сексуальное домогательство", ["трахнуть", "трaxнуть"]),
    ("сексуальное домогательство", ["вытрахать", "вытрaxать"]),
    ("сексуальное домогательство", ["порно", "пopно"]),
    ("сексуальное домогательство", ["секс", "ceкс"]),
    ("сексуальное домогательство", ["сосать", "coсать"]),
]

EXTREMISM = [
    ("экстремизм", ["террорист", "тeррорист"]),
    ("экстремизм", ["экстремист", "эkcтремист"]),
    ("экстремизм", ["джихад", "джuхад"]),
    ("экстремизм", ["убивать", "yбивать"]),
    ("экстремизм", ["взорвать", "взopвать"]),
    ("экстремизм", ["уничтожить", "уничтoжить"]),
]

TWITCH = [
    ("твич-запретка", ["куколд", "кyколд"]),
    ("твич-запретка", ["конча", "кoнча"]),
    ("твич-запретка", ["симп", "сuмп"]),
    ("твич-запретка", ["инцел", "uнцел"]),
    ("твич-запретка", ["cuckold", "cuckоld"]),
    ("твич-запретка", ["incel", "іncel"]),
    ("твич-запретка", ["simp", "sіmp"]),
    ("твич-запретка", ["virgin", "vіrgin"]),
    ("твич-запретка", ["девственник", "дeвственник"]),
    ("твич-запретка", ["cunt", "cunт"]),
]

ALL_BAD = THREATS + INSULTS + DISCRIMINATION + SEXUAL + EXTREMISM + TWITCH

def mega_detect(text):
    if not text:
        return False, ""
    
    text_lower = text.lower()
    
    for category_name, variants in ALL_BAD:
        for variant in variants:
            if variant in text_lower:
                return True, category_name
            
            no_spaces = re.sub(r'\s+', '', text_lower)
            if variant in no_spaces:
                return True, category_name
    
    return False, ""

# ============================================
# ГЛАВНЫЙ ОБРАБОТЧИК
# ============================================

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Пропускаем сообщения от бота
    if message.from_user.id == bot.get_me().id:
        return
    
    # === ЕСЛИ СООБЩЕНИЕ В ГРУППЕ ОБСУЖДЕНИЯ ===
    if message.chat.id == DISCUSSION_GROUP_ID:
        text = message.text or ""
        
        # === ПРОВЕРКА: ЭТО СИСТЕМНОЕ СООБЩЕНИЕ О НОВОМ ПОСТЕ ===
        # ID 777000 - это системный аккаунт Telegram
        # У таких сообщений нет username и они приходят от канала
        if message.from_user.id == 777000:
            # Это НОВЫЙ ПОСТ в канале - отвечаем правилами
            try:
                bot.reply_to(message, RULES)
                print("✅ Правила отправлены в ответ на новый пост")
            except Exception as e:
                print(f"❌ Ошибка отправки правил: {e}")
            return
        
        # === ПРОВЕРКА: ЭТО ПЕРЕСЛАННОЕ СООБЩЕНИЕ ИЗ КАНАЛА ===
        # Если сообщение содержит forward_from_chat или forward_from
        if message.forward_from_chat or message.forward_from:
            # Это пересланное сообщение - НЕ пересылаем обратно!
            print(f"⏭️ Пропускаем пересланное сообщение от {message.from_user.username}")
            return
        
        # === МОДЕРАЦИЯ ОБЫЧНЫХ КОММЕНТАРИЕВ ===
        is_bad, reason = mega_detect(text)
        
        if is_bad:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, f"⚠️ Удалено. Причина: **{reason}**")
                print(f"🗑️ Удалено: {reason}")
            except Exception as e:
                print(f"❌ Ошибка удаления: {e}")
            return
        
        # ССЫЛКИ
        if re.search(r'https?://\S+|www\.\S+', text):
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "⚠️ Удалено: ссылка")
                print(f"🗑️ Удалена ссылка")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            return
        
        # === ПЕРЕСЫЛАЕМ ТОЛЬКО ЕСЛИ ЭТО НЕ СИСТЕМНОЕ СООБЩЕНИЕ ===
        # И не пересланное сообщение, и не от бота
        if text and message.from_user.id != 777000 and not message.forward_from_chat:
            try:
                bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
                print(f"📩 Переслано в канал от {message.from_user.username}")
            except Exception as e:
                print(f"❌ Ошибка пересылки: {e}")
        
        return
    
    # === ЛИЧНЫЕ СООБЩЕНИЯ БОТУ ===
    if message.chat.type == "private":
        if text.startswith("/"):
            return  # команды обрабатываются выше
        bot.reply_to(message, "Напиши /start или /rules")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 БОТ ЗАПУЩЕН!")
    print(f"📌 Группа обсуждения: {DISCUSSION_GROUP_ID}")
    print("📌 При новом посте → правила в комментарии")
    print("📌 Комментарии → пересылка в канал (без флуда)")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Переподключение через 10 секунд...")
            time.sleep(10)
