import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

# Стартовое меню
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Журнал сделок", "Торговый план", "Риск-менеджмент", "Психология", "Напоминания", "Настройки"]
    keyboard.add(*[KeyboardButton(text=btn) for btn in buttons])
    await message.answer("Привет! Я твой трейд-журнал. Выбери, с чего начнём:", reply_markup=keyboard)

# Журнал сделок
@dp.message_handler(lambda message: message.text == "Журнал сделок")
async def journal_entry(message: types.Message):
    await message.answer("Введите данные по сделке:\nИнструмент, вход, выход, объём, SL, TP, комментарий...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)