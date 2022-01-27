import telebot

TOKEN = "5254187244:AAHvAXakpIHi6yKaFvHC4QFlg-KsOmLWCQM"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, "hello")

bot.polling()
