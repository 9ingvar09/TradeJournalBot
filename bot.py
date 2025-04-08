from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = "7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs"
OWNER_ID = 861463774

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message

    if user.id != OWNER_ID:
        forward = f"Новое сообщение от @{user.username or 'без ника'} (ID: {user.id}):\n{message.text}"
        await context.bot.send_message(chat_id=OWNER_ID, text=forward)
        await context.bot.send_message(chat_id=user.id, text="Спасибо! Мы скоро ответим.")
    else:
        if message.text.startswith("/ответ"):
            parts = message.text.split(" ", 2)
            if len(parts) >= 3:
                target_id = int(parts[1])
                reply_text = parts[2]
                await context.bot.send_message(chat_id=target_id, text=reply_text)
                await context.bot.send_message(chat_id=OWNER_ID, text="Ответ отправлен.")
            else:
                await message.reply_text("Формат: /ответ user_id сообщение")
        else:
            await message.reply_text("Для ответа клиенту используй: /ответ user_id сообщение")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_message))
    print("Бот запущен...")
    await app.run_polling()

# Для запуска на Render/в вебе
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_running_loop().create_task(main())
    except RuntimeError:
        asyncio.run(main())