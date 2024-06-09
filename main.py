from telegram_bot.create_bot import bot
from telegram_bot import handlers

if __name__ == '__main__':
    handlers.register_handlers(bot) # Регистрируем команды
    print('BOT START')
    bot.polling()
