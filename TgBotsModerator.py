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
    bot.reply_to(message, "🤖 Бот запущен! Добавь меня в группу обсуждения как админа.")

# ===== ЕСЛИ БОТ В ГРУППЕ ОБСУЖДЕНИЯ =====
# Этот обработчик срабатывает, когда кто-то пишет в группе (включая комментарии к постам)
@bot.message_handler(func=lambda message: True)
def moderate(message):
    # Пропускаем сообщения от бота
    if message.from_user.id == bot.get_me().id:
        return
    
    # Проверяем, что сообщение в группе/супергруппе
    if message.chat.type not in ["group", "supergroup"]:
        return
    
    # Если сообщение — это новый комментарий к посту (есть reply_to_message)
    if message.reply_to_message:
        # Если это ответ на пост из канала (у поста нет автора)
        if message.reply_to_message.from_user is None:
            # Пишем правила под каждым комментарием
            bot.reply_to(message, RULES)
            return
    
    # Если это обычное сообщение в группе — проверяем на мат/ссылку
    text = message.text or ""
    text_lower = text.lower()
    
    # Мат
    bad_words = ["хуй", "пизда", "бля", "ебать", "залупа", "мудак", "говно", "шлюха", "сука", "пидор", "гандон", "мразь", "тварь"]
    for word in bad_words:
        if word in text_lower:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "⚠️ Удалено: мат")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            return
    
    # Ссылки
    url_pattern = r'https?://\S+|www\.\S+|\S+\.\S+'
    if re.search(url_pattern, text):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: ссылка")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        return
    
    # Спам
    if "!!!!!" in text or "?????" in text:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: спам")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        return
    
    # Капс
    upper = sum(1 for c in text if c.isupper())
    if len(text) > 10 and upper / len(text) > 0.7:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "⚠️ Удалено: капс")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        return

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот запущен!")
    print("📌 Добавь меня в группу обсуждения как админа!")
    print("📌 Я буду писать правила под комментариями")
    print("📌 И удалять мат/ссылки/спам/капс")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Переподключение через 10 секунд...")
            time.sleep(10)
