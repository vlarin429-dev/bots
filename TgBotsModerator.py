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
    bot.reply_to(message, "🤖 Бот запущен! Добавь меня в группу обсуждения.")

# ===== КОМАНДА ДЛЯ ПОЛУЧЕНИЯ ID =====
@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"🆔 ID этого чата: `{message.chat.id}`")

# ===== НОВЫЙ ПОСТ В КАНАЛЕ — ПИШЕМ ПРАВИЛА В КОММЕНТЫ =====
@bot.channel_post_handler(func=lambda message: True)
def new_post(message):
    try:
        # Отправляем правила в группу обсуждения
        # Используем reply_to_message_id, чтобы ответить на сообщение о посте
        bot.send_message(
            DISCUSSION_GROUP_ID,
            RULES,
            reply_to_message_id=message.message_id
        )
        print(f"✅ Правила отправлены в обсуждение к посту {message.message_id}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        # Если не получилось ответить — просто отправляем в чат
        try:
            bot.send_message(DISCUSSION_GROUP_ID, RULES)
            print("✅ Правила отправлены в чат (без ответа)")
        except Exception as e2:
            print(f"❌ Ошибка: {e2}")

# ===== МОДЕРАЦИЯ КОММЕНТАРИЕВ =====
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
    
    # Если это сообщение о новом посте (от канала) — игнорируем
    if message.from_user.id == 777000:  # ID Telegram (системные сообщения)
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
