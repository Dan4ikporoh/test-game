import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- Настройки ---
# Укажите токен вашего бота, полученный от @BotFather
API_TOKEN = '8562700528:AAEai5V4VQgLWi94l_BPksoZBP0oO3bl2DQ' 
# URL, на котором будет запущено ваше веб-приложение (фронтенд)
WEB_APP_URL = 'https://your-unique-app-name.netlify.app' # Пример для хостинга

# --- Инициализация ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Логика Бота ---
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    """
    Отправляет приветственное сообщение и кнопку для запуска Web App.
    """
    # Создаем кнопку, которая открывает веб-приложение
    web_app_button = InlineKeyboardButton(
        text="⚔️ НАЧАТЬ БОЙ! ⚔️",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    # Создаем клавиатуру с этой кнопкой
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
    
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n\n"
        "Добро пожаловать в **FRIDE Clicker RPG**!\n\n"
        "Готов сразиться с монстрами? Нажми на кнопку ниже, чтобы начать!",
        reply_markup=keyboard
    )

async def main():
    """Запуск бота."""
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
