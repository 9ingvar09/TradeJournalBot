import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен твоего бота
BOT_TOKEN = "7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs"

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext):
    # Главное меню
    keyboard = [
        [KeyboardButton("Журнал сделок"), KeyboardButton("Торговый план")],
        [KeyboardButton("Риск-менеджмент"), KeyboardButton("Психология")],
        [KeyboardButton("Напоминания"), KeyboardButton("Настройки")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я твой трейдинг-бот. Выберите опцию:", reply_markup=reply_markup)

# Функция для обработки текста
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Журнал сделок":
        await update.message.reply_text("Введите информацию по сделке: Инструмент, Вход, Выход и т.д.")
    elif text == "Торговый план":
        await update.message.reply_text("Введите торговый план для сегодняшней сессии.")
    elif text == "Риск-менеджмент":
        await update.message.reply_text("Введите ваши настройки риск-менеджмента.")
    elif text == "Психология":
        await update.message.reply_text("Ответьте на вопросы о своем настроении и эмоциях перед торговлей.")
    elif text == "Напоминания":
        await update.message.reply_text("Настройте напоминания для своих торговых сессий.")
    elif text == "Настройки":
        await update.message.reply_text("Настройки бота: язык, таймзона и другие параметры.")
    else:
        await update.message.reply_text("Выберите одну из предложенных опций.")

# Основная функция для запуска бота
def main():
    # Создаем объект приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()