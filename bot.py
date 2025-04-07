import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from handlers import journal, plan, risk, psychology, reminders

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

# Регистрация хендлеров
journal.register_handlers(dp)
plan.register_handlers(dp)
risk.register_handlers(dp)
psychology.register_handlers(dp)
reminders.register_handlers(dp)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Выберите язык / Choose language / Оберіть мову")

if __name__ == "__main__":
    executor.start_polling(dp)