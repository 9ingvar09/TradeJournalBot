import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Устанавливаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Функция /start, которая будет приветствовать пользователя
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привет! Я твой торговый помощник. Команды: /start, /journal, /plan, /risk, /psychology, /reminders.')

# Функция для команды /journal — Журнал сделок
def journal(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Отправь данные сделки: инструмент, вход, выход, размер позиции, тип сделки.')

# Функция для команды /plan — Торговый план
def plan(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Отправь торговый план на день: инструменты, точки входа, стопы, тейки.')

# Функция для команды /risk — Риск-менеджмент
def risk(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Введите максимальный риск на день и сделку.')

# Функция для команды /psychology — Психологический контроль
def psychology(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Как ты себя чувствуешь перед торговлей? Напиши "спокоен/не спокоен".')

# Функция для команды /reminders — Напоминания
def reminders(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Я буду напоминать тебе: проверяй план, следи за эмоциями, соблюдай лимиты.')

# Основная функция, которая запускает бота
def main():
    updater = Updater(BOT_TOKEN)

    # Получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("journal", journal))
    dispatcher.add_handler(CommandHandler("plan", plan))
    dispatcher.add_handler(CommandHandler("risk", risk))
    dispatcher.add_handler(CommandHandler("psychology", psychology))
    dispatcher.add_handler(CommandHandler("reminders", reminders))

    # Запуск бота
    updater.start_polling()

    # Бот будет работать до тех пор, пока не будет остановлен
    updater.idle()

if __name__ == '__main__':
    main()