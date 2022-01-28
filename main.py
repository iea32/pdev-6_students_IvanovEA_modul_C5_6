import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество валюты>\nУвидить список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(messege: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(messege, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    values = message.text.split(" ")

    if len(values) != 3:
        raise ConvertionException("Неправильное количество параметров.")

    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount)
    # quote_ticker, base_ticker = keys[quote], keys[base]
    text = f"Цена {amount} {quote} в {base} - {total_base}"
    bot.send_message(message.chat.id, text)


bot.polling()
