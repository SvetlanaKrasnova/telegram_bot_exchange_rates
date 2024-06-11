import telebot
from telegram_bot.bot import cfg
from src.currency_conversion import CurrencyConversion
from exceptions.exceptions import APIException
from telegram_bot.bot import bot

cc = CurrencyConversion(api_key=cfg.api.x_rapid_api_key,
                        rates=cfg.rates)


def help_start(message: telebot.types.Message):
    """
    Функция по началу работы с ботом
    :param message:
    :return:
    """
    text = f'Приветствую тебя *{message.chat.username or message.chat.first_name}*!\n' \
           f'Чтобы начать работу введите команду боту в следующем формате:\n' \
           f'<имя валюты, цену которой хотите узнать>\n' \
           f'<количество переводимой валюты>\n\n' \
           f'*Пример команд:*\n' \
           f'"рубль евро 3"\n' \
           f'"доллар рубль 1"\n\n' \
           f'Увидеть список всех доступных валют можно с помощью команды /values'
    bot.reply_to(message, text, parse_mode='Markdown')


def values(message: telebot.types.Message):
    """
    Список доступных валют
    :param message:
    :return:
    """
    bot.reply_to(message,
                 'Доступные валюты:\n' + '\n'.join([f'{i}. {el}' for i, el in enumerate(list(cfg.rates.keys()),
                                                                                        start=1)]))


def convert(message: telebot.types.Message):
    """
    Функция по распознаванию команды и конвертации валюты
    :param message:
    :return:
    """
    try:
        print(f'Новый запрос пользователя "{message.chat.username or message.chat.first_name}" на конвертацию')
        values = message.text.split()
        print(f'Текст запроса: "{message.text}" (количество параметров {values.__len__()})')
        if values.__len__() != 3:
            raise APIException('Слишком много параметров')

        # Пример: рубль евро 1
        quote, base, amount = values
        total_base = cc.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote.lower().strip()} в {base.lower().strip()} - {total_base}'
        print(f'Ответ пользователю: {text}')
        bot.send_message(message.chat.id, text)


def register_handlers(bot):
    """
    Функция для регистрации наших команд боту
    :param bot: объект бота
    :return:
    """
    bot.register_message_handler(help_start, commands=['start', 'help'])
    bot.register_message_handler(values, commands=['values'])
    bot.register_message_handler(convert, content_types=['text'])
