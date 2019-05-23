import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

import db_service
import output_service
import response_service
from main import logger, ENTER_CITY, PERIOD, CITY_ENTERED

CITY_KEYBOARD = [[InlineKeyboardButton("Set favourite city", callback_data='1')]]


def settings(bot, update):
    city = db_service.users_cities[update.message.chat_id] if update.message.chat_id in db_service.users_cities \
        else '_none_'

    update.message.reply_text('Settings⚙️\n\nFavourite city: ' + city,
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=InlineKeyboardMarkup(CITY_KEYBOARD))
    return ENTER_CITY


def new_city(bot, update, user_data):
    query = update.callback_query

    bot.edit_message_text('Fine!\nNow, please, send me the name of the city.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              parse_mode=telegram.ParseMode.MARKDOWN)
    return CITY_ENTERED


def cancel(bot, update):
    update.message.reply_text('Bye bye.')
    return ConversationHandler.END


def city_entered(bot, update):
    if response_service.is_city_correct(update.message.text):
        update.message.reply_text('Favourite city added')
        db_service.add(update.message.chat_id, update.message.text)
    else:
        update.message.reply_text('I can\'t find this city😞')

    return ConversationHandler.END