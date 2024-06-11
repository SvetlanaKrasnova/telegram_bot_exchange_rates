from exceptions.exceptions import APIException
from interfaces.models import GetRequestAPI
from interfaces.api import RapidAPI


class CurrencyConversion:
    """
    Класс по конвертации валюты
    """

    def __init__(self, api_key: str, rates: dict):
        """

        :param api_key: ключ к api
        :param rates: словарь с валютами, с которыми бот работает
        """
        self.api = RapidAPI(api_key=api_key)
        self.rates = rates

    def get_price(self, quote: str, base: str, amount: str):
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
            currency_from = self.rates[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            currency_to = self.rates[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        # Обработка ошибки, если ввели не 1, а что-то другое (строку)
        try:
            _amount = float(amount)
            if _amount <= 0:
                # не конвертирует отрицательные числа или "0"
                raise ValueError()
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}"')

        return self.api.get(GetRequestAPI(**{'currency_from': currency_from,
                                             'currency_to': currency_to,
                                             'amount': amount})).result
