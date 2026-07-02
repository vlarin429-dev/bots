# -*- coding: utf-8 -*-
import telebot
import re
import time

TOKEN = "8670803464:AAE-DBwo7Nl8YoNGbDP6YPt_aUqaWdQLzqU"

bot = telebot.TeleBot(TOKEN)

# ===== УДАЛЯЕМ WEBHOOK (ОБЯЗАТЕЛЬНО!) =====
bot.remove_webhook()

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
    bot.reply_to(message, "🤖 Бот запущен! Я буду модерировать комментарии в канале.")

@bot.channel_post_handler(func=lambda message: True)
def new_post(message):
    """Новый пост в канале — пишем правила"""
    bot.send_message(message.chat.id, RULES, reply_to_message_id=message.message_id)

BAD_WORDS = ["хуй", "пизда", "бля", "ебать", "залупа", "мудак", "говно", "шлюха", "сука", "пидор", "гандон", "мразь", "тварь"]
URL_PATTERN = r'https?://\S+|www\.\S+|\S+\.\S+'

@bot.message_handler(func=lambda message: True)
def moderate(message):
    if message.from_user.id == bot.get_me().id:
        return
    
    text = message.text or ""
    text_lower = text.lower()
    
    # Мат
    for word in BAD_WORDS:
        if word in text_lower:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: мат", reply_to_message_id=message.message_id)
            return
    
    # Ссылки
    if re.search(URL_PATTERN, text):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "⚠️ Удалено: ссылка", reply_to_message_id=message.message_id)
        return
    
    # Спам
    if "!!!!!" in text or "?????" in text:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "⚠️ Удалено: спам", reply_to_message_id=message.message_id)
        return
    
    # Капс
    upper = sum(1 for c in text if c.isupper())
    if len(text) > 10 and upper / len(text) > 0.7:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "⚠️ Удалено: капс", reply_to_message_id=message.message_id)
        return

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот запущен!")
    print("📌 Режим: polling")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Переподключение через 10 секунд...")
            time.sleep(10)
