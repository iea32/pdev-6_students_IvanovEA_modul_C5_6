import json
import requests
import telebot

TOKEN = "5254187244:AAHvAXakpIHi6yKaFvHC4QFlg-KsOmLWCQM"

bot = telebot.TeleBot(TOKEN)

keys = {
    "биткоин": "BTC",
    "эфириум": "ETH",
    "доллар": "USD"
}


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
    quote, base, amount = message.text.split(" ")
    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}")
    total_base = json.loads(r.content)[keys[base]]
    text = f"Цена {amount} {quote} в {base} - {total_base}"
    bot.send_message(message.chat.id, text)


bot.polling()
