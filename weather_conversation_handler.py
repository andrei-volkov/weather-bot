import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

import db_service
import main
import output_service
import response_service

WINK_EMOJI = u"\U0001F609"

LATITUDE_KEY = 'lat'
LONGITUDE_KEY = 'lon'
CITY_KEY = 'city'

WEATHER_PERIOD_KEYBOARD = [[InlineKeyboardButton("Current", callback_data='1'),
                            InlineKeyboardButton("Full day", callback_data='2')],
                           [InlineKeyboardButton("5 days", callback_data='3')]]

WEATHER_START_MESSAGE= '*Great!*\nFirst of all, send me the name ' \
                       'of city or geolocation. Also you can add favourite city from settings. ' \
                       '\n\n_To stop this brunch -_ /cancel'

PERIOD_STATE_TEXT = '*Finally!*\nChoose period.\n\n_To stop this brunch -_ /cancel'


def start(bot, update):
    update.message.reply_text(
        'Hi!\nMy name is weatheric. \nIf curious about the weather,\nyou in the right place😉' + WINK_EMOJI)


def weather(bot, update):
    if update.message.chat_id in db_service.users_cities:
        city = db_service.users_cities[update.message.chat_id]
        inline = [[InlineKeyboardButton(city, callback_data=update.message.chat_id)]]

        update.message.reply_text(WEATHER_START_MESSAGE,
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=InlineKeyboardMarkup(inline))

    else:
        update.message.reply_text(WEATHER_START_MESSAGE,
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    return main.ENTER_CITY


def city_entered(bot, update, user_data):
    update.message.reply_text(PERIOD_STATE_TEXT,
                              reply_markup=InlineKeyboardMarkup(WEATHER_PERIOD_KEYBOARD),
                              parse_mode=telegram.ParseMode.MARKDOWN)

    user_data[CITY_KEY] = update.message['text']  # provided by tg bot library

    return main.CITY_ENTERED


def location_passed(bot, update, user_data):
    user = update.message.from_user
    user_location = update.message.location

    user_data[LONGITUDE_KEY] = str(user_location.longitude)
    user_data[LATITUDE_KEY] = str(user_location.latitude)

    main.logger.info("Whether request from %s: %f / %f",
                     user.first_name,
                     user_location.latitude,
                     user_location.longitude)

    update.message.reply_text(PERIOD_STATE_TEXT,
                              reply_markup=InlineKeyboardMarkup(WEATHER_PERIOD_KEYBOARD),
                              parse_mode=telegram.ParseMode.MARKDOWN)

    return main.PERIOD


def period_keyboard_pressed(bot, update, user_data):
    response = None

    query = update.callback_query

    bot.send_chat_action(chat_id=query.message.chat_id, action=telegram.ChatAction.TYPING)

    id = query.data

    if CITY_KEY in user_data:
        response = response_service.get_by_query_name(id, user_data[CITY_KEY])

        del user_data[CITY_KEY]
    else:
        response = response_service.get_by_query_geo(id, user_data[LATITUDE_KEY], user_data[LONGITUDE_KEY])

        del user_data[LONGITUDE_KEY]
        del user_data[LATITUDE_KEY]

    if '404' != response['cod']:
        bot.edit_message_text(output_service.output_by_id(id, response),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.edit_message_text('I can\'t find this city🙁'
                              '\n\nPlease, if the name of the city is correct, call my developer @Anrix_official',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    return ConversationHandler.END



def print_period_info(bot, update):
    update.message.reply_text('*Finally!*\nChoose period.\n\n_To stop this brunch -_ /cancel',
                              reply_markup=InlineKeyboardMarkup(WEATHER_PERIOD_KEYBOARD),
                              parse_mode=telegram.ParseMode.MARKDOWN)


def favourite_city_choosed(bot, update, user_data):
    query = update.callback_query

    key = int(query.data)
    user_data[CITY_KEY] = db_service.users_cities[key]

    bot.edit_message_text(PERIOD_STATE_TEXT,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=telegram.ParseMode.MARKDOWN,
                          reply_markup=InlineKeyboardMarkup(WEATHER_PERIOD_KEYBOARD))

    return main.PERIOD
