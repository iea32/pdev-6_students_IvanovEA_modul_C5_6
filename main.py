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

class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert (quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]

        return total_base


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
