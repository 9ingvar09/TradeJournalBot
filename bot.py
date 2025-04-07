import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Включаем логирование для отслеживания ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start для приветствия
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я готов помочь вам.')

# Основная функция для запуска бота
def main() -> None:
    # Токен вашего бота
    token = '7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs'

    # Создаем Updater и передаем ему ваш токен
    updater = Updater(token)

    # Получаем диспатчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команды /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Запуск бота
    updater.start_polling()

    # Бот будет работать, пока не будет остановлен вручную
    updater.idle()

if __name__ == '__main__':
    main()