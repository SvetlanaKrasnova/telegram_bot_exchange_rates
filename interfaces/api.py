import requests
from config.config import X_RAPID_API_KEY
from interfaces.models import *
from exceptions.exceptions import APIException


class RapidAPI:

    @staticmethod
    def get(querystring: GetRequestAPI) -> ResponseRequestAPI:
        """
        Запрос на конвертацию валюты
        :param querystring: объект с входными параметрами
        :return: объект с рзультатом
        """
        print('Запрос к rapidapi')
        host = "currency-conversion-and-exchange-rates.p.rapidapi.com"
        url = f"https://{host}/convert"

        querystring = {"from": querystring.currency_from,
                       "to": querystring.currency_to,
                       "amount": querystring.amount}

        headers = {
            "X-RapidAPI-Key": X_RAPID_API_KEY,
            "X-RapidAPI-Host": host
        }
        print(f'GET: {querystring}')
        response = requests.get(url, headers=headers, params=querystring)
        response_json = response.json()
        print(f'RESPONSE: {response_json}')
        if response.status_code == 200:
            return ResponseRequestAPI(**response_json)
        else:
            raise APIException('Не удалось обработать команду.\n'
                               'Попробуйте выполнить запрос позже.')
