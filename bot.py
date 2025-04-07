import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Создаем подключение к базе данных
conn = sqlite3.connect('trading_bot.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    trading_pair TEXT,
                    account TEXT,
                    rr REAL,
                    risk REAL,
                    result TEXT)''')
conn.commit()

# Функции для работы с базой данных
def add_trade(date, trading_pair, account, rr, risk, result):
    cursor.execute("INSERT INTO trades (date, trading_pair, account, rr, risk, result) VALUES (?, ?, ?, ?, ?, ?)", 
                   (date, trading_pair, account, rr, risk, result))
    conn.commit()

def delete_all_trades():
    cursor.execute("DELETE FROM trades")
    conn.commit()

def delete_trade_by_id(trade_id):
    cursor.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    conn.commit()

def get_all_trades():
    cursor.execute("SELECT * FROM trades")
    return cursor.fetchall()

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Добавить сделку"), KeyboardButton("Журнал сделок")],
        [KeyboardButton("Удалить все сделки"), KeyboardButton("Удалить сделку по ID")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я твой трейдинг-бот. Выберите опцию:", reply_markup=reply_markup)

# Функция для добавления сделки
async def add_trade_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("Введите данные сделки в формате: \nДата, Пара, Аккаунт, RR, Риск на сделку, Итог сделки")

# Функция для удаления всех сделок
async def delete_all_trades_handler(update: Update, context: CallbackContext):
    delete_all_trades()
    await update.message.reply_text("Все сделки были удалены.")

# Функция для удаления сделки по ID
async def delete_trade_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("Введите ID сделки для удаления:")

# Функция для отображения журнала сделок
async def view_trades_handler(update: Update, context: CallbackContext):
    trades = get_all_trades()
    if trades:
        for trade in trades:
            await update.message.reply_text(f"ID: {trade[0]}\nДата: {trade[1]}\nПара: {trade[2]}\nАккаунт: {trade[3]}\nRR: {trade[4]}\nРиск: {trade[5]}\nРезультат: {trade[6]}")
        # После отображения сделок, предложим дополнительные действия
        await update.message.reply_text("Вы можете выбрать одну из следующих опций:\nДобавить сделку, Удалить все сделки, Удалить сделку по ID.")
    else:
        await update.message.reply_text("Журнал сделок пуст. Вы можете добавить сделку.")
        # После того, как журнал пуст, предложим добавить сделку
        await update.message.reply_text("Нажмите 'Добавить сделку', чтобы добавить новую сделку.")

# Основная функция для запуска бота
def main():
    application = Application.builder().token("7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Regex('^Добавить сделку$'), add_trade_handler))
    application.add_handler(MessageHandler(filters.Regex('^Журнал сделок$'), view_trades_handler))
    application.add_handler(MessageHandler(filters.Regex('^Удалить все сделки$'), delete_all_trades_handler))
    application.add_handler(MessageHandler(filters.Regex('^Удалить сделку по ID$'), delete_trade_handler))

    application.run_polling()

if __name__ == '__main__':
    main()