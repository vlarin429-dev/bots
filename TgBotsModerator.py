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

# ===== ID ГРУППЫ ОБСУЖДЕНИЯ =====
# СЮДА ВСТАВЬ ID ГРУППЫ, ГДЕ ДОЛЖНЫ БЫТЬ КОММЕНТАРИИ
# (не канал, а группа!)
DISCUSSION_GROUP_ID = -1001234567890  # ЗАМЕНИ НА СВОЙ ID ГРУППЫ!

RULES = """
📢 **ПРАВИЛА КОММЕНТАРИЕВ**

1️⃣ Без мата и оскорблений
2️⃣ Без рекламы и ссылок
3️⃣ Без спама и флуда
4️⃣ Без капса

Нарушение = удаление комментария.
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот запущен! Я буду писать правила в обсуждения.")

# ===== НОВЫЙ ПОСТ В КАНАЛЕ — ПИШЕМ В ГРУППУ ОБСУЖДЕНИЯ =====
@bot.channel_post_handler(func=lambda message: True)
def new_post(message):
    try:
        # Отправляем правила НЕ В КАНАЛ, а В ГРУППУ ОБСУЖДЕНИЯ
        bot.send_message(
            DISCUSSION_GROUP_ID,  # Сюда!
            f"📢 **Новый пост!**\n\n{RULES}"
        )
        print(f"✅ Правила отправлены в группу обсуждения {DISCUSSION_GROUP_ID}")
    except Exception as e:
        print(f"❌ Ошибка отправки в группу: {e}")

# ===== МОДЕРАЦИЯ В ГРУППЕ ОБСУЖДЕНИЯ =====
BAD_WORDS = ["хуй", "пизда", "бля", "ебать", "залупа", "мудак", "говно", "шлюха", "сука", "пидор", "гандон", "мразь", "тварь"]
URL_PATTERN = r'https?://\S+|www\.\S+|\S+\.\S+'

@bot.message_handler(func=lambda message: True)
def moderate(message):
    # Пропускаем сообщения от бота
    if message.from_user.id == bot.get_me().id:
        return
    
    # Проверяем, что это группа обсуждения
    if message.chat.id != DISCUSSION_GROUP_ID:
        return
    
    text = message.text or ""
    text_lower = text.lower()
    
    # Мат
    for word in BAD_WORDS:
        if word in text_lower:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "⚠️ Удалено: мат")
                print(f"🗑️ Удалён мат от {message.from_user.username}")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            return
    
    # Ссылки
    if re.search(URL_PATTERN, text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: ссылка")
            print(f"🗑️ Удалена ссылка от {message.from_user.username}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        return
    
    # Спам
    if "!!!!!" in text or "?????" in text:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: спам")
            print(f"🗑️ Удалён спам от {message.from_user.username}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        return
    
    # Капс
    upper = sum(1 for c in text if c.isupper())
    if len(text) > 10 and upper / len(text) > 0.7:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: капс")
            print(f"🗑️ Удалён капс от {message.from_user.username}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        return

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот запущен!")
    print(f"📌 Группа обсуждения: {DISCUSSION_GROUP_ID}")
    print("📌 При новом посте - пишу правила в группу")
    print("📌 Удаляю мат/ссылки/спам/капс")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Переподключение через 10 секунд...")
            time.sleep(10)
