import telebot
from config.config import rates
from src.currency_conversion import CurrencyConversion
from exceptions.exceptions import APIException
from telegram_bot.create_bot import bot


def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<имя валюты, цену которой хотите узнать> ' \
           '<имя валюты, в которую нужно перевести> ' \
           '<количество переводимой валюты>\n' \
           'Увидеть список всех доступных валют можно с помощью команды /values'
    bot.reply_to(message, text)


def values(message: telebot.types.Message):
    bot.reply_to(message, 'Доступные валюты:\n' + '\n'.join(list(rates.keys())))


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


def register_handlers(bot):
    """
    Функция для регистрации наших команд боту
    :param bot: объект бота
    :return:
    """
    bot.register_message_handler(help, commands=['start', 'help'])
    bot.register_message_handler(values, commands=['values'])
    bot.register_message_handler(convert, content_types=['text'])
