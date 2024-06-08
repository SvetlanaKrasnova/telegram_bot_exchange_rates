from pydantic import BaseModel, Field
from typing import Optional, Union


class GetRequestAPI(BaseModel):
    """
    Формат запроса к api
    """
    currency_from: str = Field(default='Из какой валюты переводим')
    currency_to: str = Field(default='В какую')
    amount: Union[int, float] = Field(default=1, description='Количество переводимой валюты')


class Info(BaseModel):
    rate: float = Field(description='Результат конвертации 1 валюты')


class ResponseRequestAPI(BaseModel):
    """
    Ответ от api
    """
    result: float = Field(description='Результат конвертации amount валют')
    info: Optional[Info] = Field(default=None)
