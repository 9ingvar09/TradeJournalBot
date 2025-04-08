import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Твой Telegram ID
ADMIN_ID = 123456789  # замени на свой ID

# Инициализация базы данных SQLite
def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Сохраняем сообщение в базе данных
def save_message(user_id, username, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (user_id, username, message)
    VALUES (?, ?, ?)
    ''', (user_id, username, message))
    conn.commit()
    conn.close()

# Получаем историю сообщений
def get_history():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC')
    history = cursor.fetchall()
    conn.close()
    return history

# Получаем сообщения от клиента
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = user.username or user.first_name
    message = update.message.text
    
    # Сохраняем сообщение в базу данных
    save_message(user_id, username, message)
    
    # Пересылаем администратору (тебе)
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"[ID: {user_id}] @{username}:\n{message}")

# Отправляем ответ клиенту
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Формат: /reply <user_id> <текст>")
        return

    user_id = int(args[0])
    reply_text = " ".join(args[1:])
    
    # Отправляем ответ клиенту
    await context.bot.send_message(chat_id=user_id, text=f"Менеджер: {reply_text}")
    
    # Сохраняем ответ в базе данных
    save_message(ADMIN_ID, 'Manager', reply_text)
    
    await update.message.reply_text(f"Ответ отправлен пользователю {user_id}: {reply_text}")

# Получаем историю переписки
async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = get_history()
    if not history:
        await update.message.reply_text("История переписки пуста.")
        return
    
    # Формируем текст истории
    history_text = ""
    for msg in history:
        history_text += f"ID: {msg[1]} @{msg[2]}: {msg[3]}\n{msg[4]}\n\n"

    # Отправляем историю переписки
    await update.message.reply_text(history_text)

async def main():
    init_db()  # Инициализация базы данных

    app = ApplicationBuilder().token("7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs
").build()

    # Обработчики сообщений и команд
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(CommandHandler("history", history_command))  # Команда для просмотра истории

    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())