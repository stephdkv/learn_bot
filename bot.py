import logging
import settings

from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment, anketa_dontknow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import (greet_user, talk_to_me, user_coordinates, send_cat_pictures,
                      guess_number)

logging.basicConfig(filename='bot.log', level=logging.INFO, encoding='utf-8')

def main():
    mybot = Updater(settings.API_KEY, use_context = True,)

    anketa = ConversationHandler(
        entry_points = [
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
            ],
        states = {'name': [MessageHandler(Filters.text, anketa_name)],
                  'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
                  'comment': [
                    CommandHandler('skip', anketa_skip),
                    MessageHandler(Filters.text, anketa_comment)
                    ]
                  },
        fallbacks = [MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
                     anketa_dontknow)]
    )

    

    dp = mybot.dispatcher
    dp.add_handler(anketa)
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