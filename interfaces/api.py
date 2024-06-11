import requests
from interfaces.models import *
from exceptions.exceptions import APIException


class RapidAPI:
    def __init__(self, api_key: str):
        """

        :param api_key: Ключ для работы с api
        """
        self.api_key = api_key

    def get(self, querystring: GetRequestAPI) -> ResponseRequestAPI:
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
            "X-RapidAPI-Key": self.api_key,
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
