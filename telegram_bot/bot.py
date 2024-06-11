import telebot
from src.utils.config_loader.config_loader import Config

cfg = Config.from_yaml('config/config.yaml')

# Создаем экземпляр бота тут (для взаимоимпорта)
bot = telebot.TeleBot(cfg.bot.token)
