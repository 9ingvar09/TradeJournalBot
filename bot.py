import telebot

# Токен твоего бота
TOKEN = "7398609388:AAHpGPlqH1qW4Hx3SsdyYDtqT0PS7EXy-zs"

bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я твой торговый журнал.")

# Пример обработки текстовых сообщений
@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.send_message(message.chat.id, message.text)

# Запуск бота
bot.polling()