import json
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Функции для работы с базой данных (аккаунты)
def load_accounts():
    try:
        with open("accounts.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_accounts(accounts):
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

def add_account(account_id, account_name):
    accounts = load_accounts()
    accounts[account_id] = {"name": account_name, "balance": 1000, "trades": 0, "pairs": []}
    save_accounts(accounts)

def delete_account(account_id):
    accounts = load_accounts()
    if account_id in accounts:
        del accounts[account_id]
        save_accounts(accounts)

# Начальная функция, которая запускает бота
def start(update, context):
    keyboard = [
        [KeyboardButton("Менеджмент аккаунтов"), KeyboardButton("Статистика аккаунтов")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Привет! Выберите опцию:", reply_markup=reply_markup)

# Обработчик для кнопки "Менеджмент аккаунтов"
def manage_accounts(update, context):
    keyboard = [
        [KeyboardButton("Добавить аккаунт"), KeyboardButton("Удалить аккаунт")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Выберите опцию для управления аккаунтами:", reply_markup=reply_markup)

# Обработчик для кнопки "Добавить аккаунт"
def add_account_command(update, context):
    update.message.reply_text("Введите ID аккаунта:")
    return "WAITING_FOR_ACCOUNT_ID"

# Обработчик для получения ID аккаунта и добавления
def handle_account_id(update, context):
    account_id = update.message.text
    context.user_data['account_id'] = account_id
    update.message.reply_text("Введите название аккаунта:")
    return "WAITING_FOR_ACCOUNT_NAME"

# Обработчик для получения имени аккаунта и добавления
def handle_account_name(update, context):
    account_name = update.message.text
    account_id = context.user_data['account_id']
    add_account(account_id, account_name)
    update.message.reply_text(f"Аккаунт {account_name} с ID {account_id} добавлен.")
    return ConversationHandler.END

# Обработчик для кнопки "Удалить аккаунт"
def delete_account_command(update, context):
    update.message.reply_text("Введите ID аккаунта для удаления:")
    return "WAITING_FOR_ACCOUNT_ID_TO_DELETE"

# Обработчик для удаления аккаунта
def handle_account_delete(update, context):
    account_id = update.message.text
    delete_account(account_id)
    update.message.reply_text(f"Аккаунт с ID {account_id} удален.")
    return ConversationHandler.END

# Обработчик для статистики
def show_statistics(update, context):
    accounts = load_accounts()
    statistics_text = "Статистика по аккаунтам:\n"
    for account_id, account_info in accounts.items():
        statistics_text += f"\nАккаунт ID: {account_id}, Название: {account_info['name']}, Баланс: {account_info['balance']}, Количество сделок: {account_info['trades']}, Пары: {len(account_info['pairs'])}"
    update.message.reply_text(statistics_text)

# Главная функция
def main():
    updater = Updater("7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs"), use_context=True)  # Замените ВАШ_ТОКЕН на свой токен
    dp = updater.dispatcher

    # Диалог с пользователем
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "WAITING_FOR_ACCOUNT_ID": [MessageHandler(Filters.text & ~Filters.command, handle_account_id)],
            "WAITING_FOR_ACCOUNT_NAME": [MessageHandler(Filters.text & ~Filters.command, handle_account_name)],
            "WAITING_FOR_ACCOUNT_ID_TO_DELETE": [MessageHandler(Filters.text & ~Filters.command, handle_account_delete)],
        },
        fallbacks=[],
    )

    dp.add_handler(conversation_handler)
    dp.add_handler(MessageHandler(Filters.regex("Менеджмент аккаунтов"), manage_accounts))
    dp.add_handler(MessageHandler(Filters.regex("Статистика аккаунтов"), show_statistics))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()