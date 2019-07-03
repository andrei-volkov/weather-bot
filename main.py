import logging
import threading
import time

import schedule
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)

from service import db_service, predictor_service

token = 'bot_token'

logger = logging.getLogger(__name__)

city, period = range(2)
category, data_entered = range(2)
prediction_params_entered = range(1)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    from conversation_handler import predict_conversation_handler, main_conversation_handler, \
        weather_conversation_handler, \
        settings_conversation_handler

    updater = Updater(token, use_context=True)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('weather', weather_conversation_handler.start)],

        states={
            city: [CallbackQueryHandler(weather_conversation_handler.favorite_city_branch),
                   MessageHandler(Filters.text, weather_conversation_handler.city_branch),
                   MessageHandler(Filters.location, weather_conversation_handler.location_branch)],

            period: [CallbackQueryHandler(weather_conversation_handler.period_entered)],
        },

        fallbacks=[CommandHandler('cancel', main_conversation_handler.cancel)]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('settings', settings_conversation_handler.start)],

        states={
            category: [CallbackQueryHandler(settings_conversation_handler.button_clicked)],
            data_entered: [MessageHandler(Filters.text, settings_conversation_handler.data_entered,
                                          pass_job_queue=True, pass_chat_data=True)]
        },

        fallbacks=[CommandHandler('cancel', main_conversation_handler.cancel)]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('predict', predict_conversation_handler.start)],

        states={
            prediction_params_entered: [MessageHandler(Filters.text, predict_conversation_handler.prediction)]
        },

        fallbacks=[CommandHandler('cancel', main_conversation_handler.cancel)]
    ))

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
