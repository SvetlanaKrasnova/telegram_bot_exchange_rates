import telebot
from config.config import rates, TOKEN
from src.currency_conversion import CurrencyConversion
from exceptions.exceptions import APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handlers(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<имя валюты, цену которой хотите узнать> ' \
           '<имя валюты, в которую нужно перевести> ' \
           '<количество переводимой валюты>\n' \
           'Увидеть список всех доступных валют можно с помощью команды /values'
    bot.reply_to(message, text)


@bot.message_handlers(commands=['values'])
def values(message: telebot.types.Message):
    bot.reply_to(message, 'Доступные валюты:' + '\n'.join(list(rates.keys())))


@bot.message_handlers(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if values.__len__() != 3:
            raise APIException('Слишком много параметров')

        # Пример: рубль евро 1
        quote, base, amount = values
        total_base = CurrencyConversion.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.send_message(message.chat.id, f'Цена {amount} {quote} в {base} - {total_base}')


# start
print('BOT START')
bot.polling()
