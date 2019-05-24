import logging
import threading
import time

import schedule
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)

import db_service
import main_conversation_handler
import predict_conversation_handler
import predictor_service
import settings_conversation_handler
import weather_conversation_handler

logger = logging.getLogger(__name__)

CITY, PERIOD = range(2)

ENTER_CITY, CITY_ENTERED = range(2)

PREDICT_DATA_ENTERED = range(1)

TOKEN = '847955543:AAFlUKvjw2gi5aZ5IVQlQlYxnUXOtl2rJCU'

UPDATER = None


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN, use_context=True)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    dp = updater.dispatcher

    weather_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('weather', weather_conversation_handler.weather)],

        states={
            CITY: [CallbackQueryHandler(weather_conversation_handler.favourite_city_choosed),
                   MessageHandler(Filters.text, weather_conversation_handler.city_entered),
                   MessageHandler(Filters.location, weather_conversation_handler.location_passed)],

            PERIOD: [CallbackQueryHandler(weather_conversation_handler.period_keyboard_pressed)],
        },

        fallbacks=[CommandHandler('cancel', main_conversation_handler.cancel)]
    )

    settings_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('settings', settings_conversation_handler.settings)],

        states={
            ENTER_CITY: [CallbackQueryHandler(settings_conversation_handler.button_clicked)],
            CITY_ENTERED: [MessageHandler(Filters.text, settings_conversation_handler.data_entered,
                                          pass_job_queue=True,
                                          pass_chat_data=True)]
        },

        fallbacks=[CommandHandler('cancel', main_conversation_handler.cancel)]
    )

    predictor_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('predict', predict_conversation_handler.predict)],

        states={
            PREDICT_DATA_ENTERED: [MessageHandler(Filters.text, predict_conversation_handler.get_predict)]
        },

        fallbacks=[CommandHandler('cancel', main_conversation_handler.cancel)]
    )

    dp.add_handler(weather_conv_handler)
    dp.add_handler(settings_conv_handler)
    dp.add_handler(predictor_conv_handler)

    dp.add_handler(CommandHandler('start', main_conversation_handler.start))
    dp.add_handler(CommandHandler('help', main_conversation_handler.help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


def schedule_polling():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    db_service.init()
    predictor_service.init()

    thread2 = threading.Thread(target=schedule_polling)
    thread2.start()

    main()
