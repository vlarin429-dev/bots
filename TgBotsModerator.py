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
# НАЙДИ ID СВОЕЙ ГРУППЫ (напиши /getid в группе)
DISCUSSION_GROUP_ID = -1002054714983  # ЗАМЕНИ НА СВОЙ ID!

# ===== ПРАВИЛА =====
RULES = """Запрещено 🟡
1. Любой спам, реклама, ссылки
2. Любые материалы 18+
3. Распространение личных данных"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот запущен! Добавь меня в группу обсуждения и сделай админом.")

# ===== КОМАНДА ДЛЯ ПОЛУЧЕНИЯ ID =====
@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"🆔 ID этого чата: `{message.chat.id}`")

# ===== ГЛАВНЫЙ ОБРАБОТЧИК СООБЩЕНИЙ В ГРУППЕ =====
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Пропускаем сообщения от бота
    if message.from_user.id == bot.get_me().id:
        return
    
    # Проверяем, что это группа обсуждения
    if message.chat.id != DISCUSSION_GROUP_ID:
        return
    
    # Проверяем, есть ли в сообщении ссылка на канал
    # Это означает, что кто-то поделился постом из канала (или системное сообщение)
    if message.text and ("t.me/" in message.text or "telegram" in message.text.lower()):
        # Отправляем правила в ответ на это сообщение
        try:
            bot.reply_to(message, RULES)
            print(f"✅ Правила отправлены в ответ на сообщение {message.message_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки правил: {e}")
        return
    
    # ===== МОДЕРАЦИЯ КОММЕНТАРИЕВ =====
    text = message.text or ""
    text_lower = text.lower()
    
    BAD_WORDS = ["хуй", "пизда", "бля", "ебать", "залупа", "мудак", "говно", "шлюха", "сука", "пидор", "гандон", "мразь", "тварь"]
    URL_PATTERN = r'https?://\S+|www\.\S+|\S+\.\S+'
    
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
    print("📌 При новом посте - пишу правила в обсуждение")
    print("📌 Удаляю мат/ссылки/спам/капс")
    print("=" * 50)
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"[ERROR] {e}")
            print("[INFO] Переподключение через 10 секунд...")
            time.sleep(10)
