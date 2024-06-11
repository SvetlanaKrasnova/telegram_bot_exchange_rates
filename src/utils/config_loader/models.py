from pydantic import BaseModel


class RootModel(BaseModel):
    class Config:
        arbitraty_types_allowed = True


class Bot(RootModel):
    token: str


class API(RootModel):
    x_rapid_api_key: str


class ConfigModel(RootModel):
    bot: Bot
    api: API
    rates: dict
