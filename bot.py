import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from handlers.trade_journal import trade_journal_handler
from handlers.trade_plan import trade_plan_handler
from handlers.risk_management import risk_management_handler
from handlers.psychology import psychology_handler
from handlers.reminders import reminders_handler

# Настроим логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Команды
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Trade Journal Bot! Type /help for more info.")

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("List of commands: /trade_journal, /trade_plan, /risk_management, /psychology, /reminders")

def main():
    # Токен для бота
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)

    # Получаем диспетчера
    dp = updater.dispatcher

    # Команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("trade_journal", trade_journal_handler))
    dp.add_handler(CommandHandler("trade_plan", trade_plan_handler))
    dp.add_handler(CommandHandler("risk_management", risk_management_handler))
    dp.add_handler(CommandHandler("psychology", psychology_handler))
    dp.add_handler(CommandHandler("reminders", reminders_handler))

    # Логирование ошибок
    dp.add_error_handler(lambda update, context: logger.warning(f"Error: {context.error}"))

    # Стартуем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()