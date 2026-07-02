# -*- coding: utf-8 -*-
import telebot
import re
import time
import threading

TOKEN = "8670803464:AAE-DBwo7Nl8YoNGbDP6YPt_aUqaWdQLzqU"

bot = telebot.TeleBot(TOKEN)

# ===== УДАЛЯЕМ WEBHOOK =====
try:
    bot.remove_webhook()
    print("✅ Webhook удалён")
except Exception as e:
    print(f"⚠️ Ошибка удаления webhook: {e}")

RULES = """
📢 **ПРАВИЛА КОММЕНТАРИЕВ**

1️⃣ Без мата и оскорблений
2️⃣ Без рекламы и ссылок
3️⃣ Без спама и флуда
4️⃣ Без капса

Нарушение = удаление комментария.
"""

# ===== КОГДА ПОСТ В КАНАЛЕ =====
@bot.channel_post_handler(func=lambda message: True)
def new_post(message):
    try:
        # Отправляем правила в группу обсуждения (если она привязана)
        # Используем reply_to_message_id, чтобы ответить на сообщение о новом посте
        bot.send_message(
            message.chat.id, 
            RULES, 
            reply_to_message_id=message.message_id
        )
        print(f"✅ Правила отправлены в обсуждение к посту {message.message_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки правил: {e}")
        # Если не получилось ответить на пост, отправляем просто в чат
        try:
            bot.send_message(message.chat.id, RULES)
            print(f"✅ Правила отправлены в чат (без ответа)")
        except Exception as e2:
            print(f"❌ Ошибка: {e2}")

# ===== КОГДА КТО-ТО ПИШЕТ В ГРУППЕ ОБСУЖДЕНИЯ =====
BAD_WORDS = ["хуй", "пизда", "бля", "ебать", "залупа", "мудак", "говно", "шлюха", "сука", "пидор", "гандон", "мразь", "тварь"]
URL_PATTERN = r'https?://\S+|www\.\S+|\S+\.\S+'

@bot.message_handler(func=lambda message: True)
def moderate(message):
    # Пропускаем сообщения от бота
    if message.from_user.id == bot.get_me().id:
        return
    
    # Проверяем, что сообщение в группе/супергруппе (обсуждение)
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    text = message.text or ""
    text_lower = text.lower()
    
    # ===== МАТ =====
    for word in BAD_WORDS:
        if word in text_lower:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "⚠️ Удалено: мат")
                print(f"🗑️ Удалён мат от {message.from_user.username}")
            except Exception as e:
                print(f"❌ Ошибка удаления: {e}")
            return
    
    # ===== ССЫЛКИ =====
    if re.search(URL_PATTERN, text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: ссылка")
            print(f"🗑️ Удалена ссылка от {message.from_user.username}")
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
        return
    
    # ===== СПАМ =====
    if "!!!!!" in text or "?????" in text:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: спам")
            print(f"🗑️ Удалён спам от {message.from_user.username}")
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
        return
    
    # ===== КАПС =====
    upper = sum(1 for c in text if c.isupper())
    if len(text) > 10 and upper / len(text) > 0.7:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: капс")
            print(f"🗑️ Удалён капс от {message.from_user.username}")
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
        return

# ===== ДЛЯ ПРОВЕРКИ (КОМАНДА /start) =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот запущен! Я буду писать правила в обсуждение к каждому посту.")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот запущен!")
    print("📌 При новом посте в канале - пишу правила в обсуждение")
    print("📌 Удаляю мат/ссылки/спам/капс в комментариях")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Переподключение через 10 секунд...")
            time.sleep(10)
