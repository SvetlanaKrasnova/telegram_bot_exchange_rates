import requests
import lxml.html
from config.config import rates
from exceptions.exceptions import APIException

class XRatesCurrencyConversion:
    """
    Взаимодействие с x-rates.com. Там беру актуальный курс валюты
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
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            currency_from = rates[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            currency_to = rates[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        # Обработка ошибки, если ввели не 1, а что-то другое (строку)
        try:
            _amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}"')

        html = requests.get(
            f'https://www.x-rates.com/calculator/?from={currency_from}&to={currency_to}&amount={amount}')
        tree = lxml.html.document_fromstring(html.content)

        output_rslt = tree.find('.//span[@class="ccOutputRslt"]').text
        output_trail = tree.find('.//span[@class="ccOutputTrail"]').text
        return f'{output_rslt}{output_trail}'.strip()
