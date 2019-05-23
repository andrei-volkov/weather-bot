import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

import main
import print_service
import weather_service

WINK_EMOJI = u"\U0001F609"

LATITUDE_KEY = 'lat'
LONGITUDE_KEY = 'lon'
CITY_KEY = 'city'

WEATHER_PERIOD_REPLY_MARKUP = [['Current📗', 'Week📕']]

WEATHER_TEST_KEYBOARD = [[InlineKeyboardButton("Current📗", callback_data='1'),
                          InlineKeyboardButton("Week📕", callback_data='2')]]


def start(bot, update):
    update.message.reply_text(
        'Hi!\nMy name is weatheric. \nIf curious about the weather,\nyou in the right place.' + WINK_EMOJI)


def weather(bot, update):
    update.message.reply_text('Great!\nFirst of all, send me the name of your city(not implemented) or your geolocation'
                              '.\nTo stop this brunch - /cancel')
    return main.CITY


def city_entered(bot, update, user_data):
    update.message.reply_text('Finally!\nChoose period.\nTo stop this brunch - /cancel',
                              reply_markup=InlineKeyboardMarkup(WEATHER_TEST_KEYBOARD))

    user_data[CITY_KEY] = update.message['text']  # provided by tg bot library

    return main.PERIOD


def location_passed(bot, update, user_data):
    user = update.message.from_user
    user_location = update.message.location

    user_data[LONGITUDE_KEY] = str(user_location.longitude)
    user_data[LATITUDE_KEY] = str(user_location.latitude)

    main.logger.info("Whether request from %s: %f / %f",
                     user.first_name,
                     user_location.latitude,
                     user_location.longitude)

    update.message.reply_text('Finally!\nChoose period.\nTo stop this brunch - /cancel',
                              reply_markup=ReplyKeyboardMarkup(WEATHER_PERIOD_REPLY_MARKUP, one_time_keyboard=True))

    return main.PERIOD


def period_keyboard_pressed(bot, update, user_data):
    response = None

    query = update.callback_query

    bot.send_chat_action(chat_id=query.message.chat_id, action=telegram.ChatAction.TYPING)

    if CITY_KEY in user_data:
        response = weather_service.get_weather_by_city_name(user_data[CITY_KEY])

        del user_data[CITY_KEY]
    else:
        response = weather_service.get_weather_by_geo(user_data[LATITUDE_KEY], user_data[LONGITUDE_KEY])

        del user_data[LONGITUDE_KEY]
        del user_data[LATITUDE_KEY]

    if '404' != response['cod']:
        bot.edit_message_text(print_service.current_weather(response),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    else:
        bot.edit_message_text('**I can''t find this city.**\nPlease, if the name of city is right, call my developer '
                              '@Anrix_official',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    main.logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
