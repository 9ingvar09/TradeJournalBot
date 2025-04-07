import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Создаем или открываем базу данных
def create_db():
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    # Создание таблиц для аккаунтов и статистики
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT NOT NULL,
            account_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            account_id TEXT NOT NULL,
            profit REAL,
            rr REAL,
            trades INTEGER,
            pairs INTEGER,
            PRIMARY KEY (account_id)
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления аккаунта в базу данных
def add_account_to_db(account_id: str, account_name: str):
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO accounts (account_id, account_name) VALUES (?, ?)
    ''', (account_id, account_name))
    conn.commit()
    conn.close()

# Функция для удаления аккаунта из базы данных
def delete_account_from_db(account_id: str):
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM accounts WHERE account_id = ?
    ''', (account_id,))
    conn.commit()
    conn.close()

# Функция для получения всех аккаунтов
def get_all_accounts():
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT account_id, account_name FROM accounts')
    accounts = cursor.fetchall()
    conn.close()
    return accounts

# Функция для получения статистики аккаунта
def get_account_statistics(account_id: str):
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT profit, rr, trades, pairs FROM statistics WHERE account_id = ?', (account_id,))
    stats = cursor.fetchone()
    conn.close()
    return stats

# Функция для команды /start
def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Менеджмент аккаунтов"), KeyboardButton("Статистика")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Привет! Я ваш трейдер-бот! Выберите действие:', reply_markup=reply_markup)

# Функция для обработки команды "Менеджмент аккаунтов"
def manage_accounts(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Добавить аккаунт"), KeyboardButton("Удалить аккаунт")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Вы выбрали менеджмент аккаунтов. Доступные действия:', reply_markup=reply_markup)

# Функция для обработки команды "Статистика"
def statistics(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("График доходности"), KeyboardButton("RR")],
        [KeyboardButton("Количество сделок"), KeyboardButton("Пары")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Вы выбрали статистику. Доступные данные:', reply_markup=reply_markup)

# Функция для добавления аккаунта
def add_account(update: Update, context: CallbackContext):
    # Пример: Ввод данных аккаунта
    account_id = "12345"  # Это должно быть введено пользователем
    account_name = "Test Account"  # Это тоже введет пользователь
    add_account_to_db(account_id, account_name)
    update.message.reply_text(f"Аккаунт {account_name} добавлен!")

# Функция для удаления аккаунта
def delete_account(update: Update, context: CallbackContext):
    account_id = "12345"  # Здесь пользователь введет ID аккаунта для удаления
    delete_account_from_db(account_id)
    update.message.reply_text(f"Аккаунт с ID {account_id} удален!")

# Функция для отображения статистики
def display_statistics(update: Update, context: CallbackContext):
    account_id = "12345"  # Здесь пользователь может ввести ID аккаунта
    stats = get_account_statistics(account_id)
    if stats:
        profit, rr, trades, pairs = stats
        update.message.reply_text(f"Статистика для аккаунта {account_id}:\n"
                                  f"Прибыль: {profit}\nRR: {rr}\nКоличество сделок: {trades}\nПары: {pairs}")
    else:
        update.message.reply_text("Статистика не найдена.")

# Главная функция
def main():
    create_db()  # Создаем базу данных и таблицы
    updater = Updater("7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs", use_context=True)
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    dp.add_handler(MessageHandler(Filters.regex('^Менеджмент аккаунтов$'), manage_accounts))
    dp.add_handler(MessageHandler(Filters.regex('^Статистика$'), statistics))
    dp.add_handler(MessageHandler(Filters.regex('^Добавить аккаунт$'), add_account))
    dp.add_handler(MessageHandler(Filters.regex('^Удалить аккаунт$'), delete_account))
    dp.add_handler(MessageHandler(Filters.regex('^График доходности$'), graph))
    dp.add_handler(MessageHandler(Filters.regex('^RR$'), rr))
    dp.add_handler(MessageHandler(Filters.regex('^Количество сделок$'), trades))
    dp.add_handler(MessageHandler(Filters.regex('^Пары$'), pairs))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()