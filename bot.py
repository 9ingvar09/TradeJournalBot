from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import sqlite3

# Создание базы данных
def create_db():
    conn = sqlite3.connect('trader_bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_name TEXT,
                    account_id INTEGER,
                    trades INTEGER,
                    rr REAL,
                    graph BLOB)''')
    conn.commit()
    conn.close()

# Обработчик команды /start
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f'Привет, {user.first_name}! Выберите одну из опций.')

    keyboard = [
        [InlineKeyboardButton("Менеджмент аккаунтов", callback_data='manage_accounts')],
        [InlineKeyboardButton("Статистика", callback_data='statistics')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Что вы хотите сделать?', reply_markup=reply_markup)

# Функции для кнопок
def manage_accounts(update, context):
    keyboard = [
        [InlineKeyboardButton("Добавить аккаунт", callback_data='add_account')],
        [InlineKeyboardButton("Удалить аккаунт", callback_data='delete_account')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.edit_text('Выберите действие с аккаунтами:', reply_markup=reply_markup)

def add_account(update, context):
    update.callback_query.message.edit_text('Введите информацию об аккаунте.')
    # Здесь можно добавить логику добавления аккаунта в базу данных

def delete_account(update, context):
    update.callback_query.message.edit_text('Введите ID аккаунта для удаления.')
    # Логика удаления аккаунта

def statistics(update, context):
    keyboard = [
        [InlineKeyboardButton("График доходности", callback_data='graph')],
        [InlineKeyboardButton("RR", callback_data='rr')],
        [InlineKeyboardButton("Количество сделок", callback_data='trades')],
        [InlineKeyboardButton("Пары", callback_data='pairs')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.edit_text('Выберите статистику:', reply_markup=reply_markup)

def graph(update, context):
    update.callback_query.message.edit_text('График доходности.')
    # Логика отображения графика

def rr(update, context):
    update.callback_query.message.edit_text('RR.')
    # Логика отображения RR

def trades(update, context):
    update.callback_query.message.edit_text('Количество сделок.')
    # Логика отображения количества сделок

def pairs(update, context):
    update.callback_query.message.edit_text('Пары.')
    # Логика отображения пар

def main():
    create_db()  # Создаем базу данных и таблицы
    updater = Updater("7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs", use_context=True)
    
    dp = updater.dispatcher  # Здесь правильный отступ

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    dp.add_handler(CallbackQueryHandler(manage_accounts, pattern='^manage_accounts$'))
    dp.add_handler(CallbackQueryHandler(statistics, pattern='^statistics$'))
    dp.add_handler(CallbackQueryHandler(add_account, pattern='^add_account$'))
    dp.add_handler(CallbackQueryHandler(delete_account, pattern='^delete_account$'))
    dp.add_handler(CallbackQueryHandler(graph, pattern='^graph$'))
    dp.add_handler(CallbackQueryHandler(rr, pattern='^rr$'))
    dp.add_handler(CallbackQueryHandler(trades, pattern='^trades$'))
    dp.add_handler(CallbackQueryHandler(pairs, pattern='^pairs$'))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()