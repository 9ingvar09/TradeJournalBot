import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Включаем логирование для отслеживания ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start для приветствия
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я готов помочь вам.')

# Основная функция для запуска бота
def main() -> None:
    # Токен вашего бота
    token = '7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs'

    # Создаем приложение и передаем ему ваш токен
    application = Application.builder().token(token).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler('start', start))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()