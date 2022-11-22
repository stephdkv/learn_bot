import logging
import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import (greet_user, talk_to_me, user_coordinates, send_cat_pictures,
                      guess_number)

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(settings.API_KEY, use_context = True,)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_pictures))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_pictures))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()
if __name__ == '__main__':
    main()