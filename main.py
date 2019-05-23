import logging
import pymongo

import db_service
import favorite_city_conversation_handler
import weather_conversation_handler
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

logger = logging.getLogger(__name__)

# weather conv states
CITY, PERIOD = range(2)

# favorite city conv states
NOT_IMPLEMENTED = 0

TOKEN = '847955543:AAFlUKvjw2gi5aZ5IVQlQlYxnUXOtl2rJCU'


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def help(bot, update):
    update.message.reply_text('List of commands:\n/add - add favorite city\n/weather - show the weather')


def main():
    updater = Updater(TOKEN)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    dp = updater.dispatcher

    weather_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('weather', weather_conversation_handler.weather)],

        states={
            CITY: [MessageHandler(Filters.text, weather_conversation_handler.city_entered, pass_user_data=True),
                   MessageHandler(Filters.location, weather_conversation_handler.location_passed, pass_user_data=True)],

            PERIOD: [CallbackQueryHandler(weather_conversation_handler.period_keyboard_pressed, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancel', weather_conversation_handler.cancel)]
    )

    favorite_city_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', favorite_city_conversation_handler.add)],

        states={
            NOT_IMPLEMENTED: [MessageHandler(Filters.text, favorite_city_conversation_handler.cancel)]
        },

        fallbacks=[CommandHandler('cancel', weather_conversation_handler.cancel)]
    )

    dp.add_handler(weather_conv_handler)
    dp.add_handler(favorite_city_conv_handler)
    dp.add_handler(CommandHandler('help', help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    for i in db_service.get_all_users():
        print(i)

    main()
