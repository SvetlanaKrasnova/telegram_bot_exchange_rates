import os
import yaml
import telebot
import requests
from pathlib import Path


class Config():
    @classmethod
    def from_yaml(self, file: str):
        file = Path(file)
        if not os.path.exists(str(file)):
            raise ConfigLoadException('Некорректный путь к yaml файлу.\n'
                                      'Пожалуйста, убедитесь что файл существует.')

        with open(file, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return config


cfg = Config.from_yaml('config/config.yaml')


class APIException(Exception):
    pass


class ConfigLoadException(Exception):
    pass


class RapidAPI:

    @staticmethod
    def get(querystring: dict):
        """
        Запрос на конвертацию валюты
        :param querystring: объект с входными параметрами
        :return: объект с рзультатом
        """
        print('Запрос к rapidapi')
        host = "currency-conversion-and-exchange-rates.p.rapidapi.com"
        url = f"https://{host}/convert"

        querystring = {"from": querystring['currency_from'],
                       "to": querystring['currency_to'],
                       "amount": querystring['amount']}

        headers = {
            "X-RapidAPI-Key": cfg['api']['x_rapid_api_key'],
            "X-RapidAPI-Host": host
        }
        print(f'GET: {querystring}')
        response = requests.get(url, headers=headers, params=querystring)
        response_json = response.json()
        print(f'RESPONSE: {response_json}')
        if response.status_code == 200:
            return response_json
        else:
            raise APIException('Не удалось обработать команду.\n'
                               'Попробуйте выполнить запрос позже.')


class CurrencyConversion:
    """
    Класс по конвертации валюты
    """

    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        """
        Метод возвращает возвращает нужную сумму в валюте
        :param quote: имя валюты, цену в которой надо узнать
        :param base: имя валюты, цену на которую надо узнать
        :param amount: количество переводимой валюты
        :return:
        """
        quote = quote.lower().strip()
        base = base.lower().strip()
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты.')

        try:
            currency_from = cfg['rates'][quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            currency_to = cfg['rates'][base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        # Обработка ошибки, если ввели не 1, а что-то другое (строку)
        try:
            if amount.__contains__(','):
                amount = amount.replace(',', '.')
                print(f'В количестве содержится ",". Пробуем преобразовать и получить курс от "{amount}"')

            _amount = float(amount)
            if _amount <= 0:
                # не конвертирует отрицательные числа или "0"
                raise ValueError()
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}"')

        return RapidAPI.get({'currency_from': currency_from,
                             'currency_to': currency_to,
                             'amount': amount})['result']


# ------------ Сам бот ------------

bot = telebot.TeleBot(cfg['bot']['token'])


@bot.message_handler(commands=['start', 'help'])
def help_start(message: telebot.types.Message):
    """
    Функция по началу работы с ботом
    :param message:
    :return:
    """
    text = f'Приветствую тебя *{message.chat.username or message.chat.first_name}*!\n' \
           f'Чтобы начать работу введите команду боту в следующем формате:\n' \
           f'<имя валюты, цену которой хотите узнать>\n' \
           f'<имя валюты, в которую нужно перевести>\n' \
           f'<количество переводимой валюты>\n\n' \
           f'*Пример команд:*\n' \
           f'"рубль евро 3"\n' \
           f'"доллар рубль 1"\n\n' \
           f'Увидеть список всех доступных валют можно с помощью команды /values'
    bot.reply_to(message, text, parse_mode='Markdown')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    """
    Список доступных валют
    :param message:
    :return:
    """
    bot.reply_to(message,
                 'Доступные валюты:\n' + '\n'.join([f'{i}. {el}' for i, el in enumerate(list(cfg['rates'].keys()),
                                                                                        start=1)]))


@bot.message_handler(content_types=['text'])
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
            raise APIException('Некорректный запрос.\n'
                               'Чтобы узнать, как пользоваться ботом наберите команду /help')

        # Пример: рубль евро 1
        quote, base, amount = values
        total_base = CurrencyConversion.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, str(e))

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote.lower().strip()} в {base.lower().strip()} - {total_base}'
        print(f'Ответ пользователю: {text}')
        bot.send_message(message.chat.id, text)


print('BOT START')
bot.polling()
