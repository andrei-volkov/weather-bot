from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

import main
import weather_service

WINK_EMOJI = u"\U0001F609"

LATITUDE_KEY = 'lat'
LONGITUDE_KEY = 'lon'
CITY_KEY = 'city'

WEATHER_PERIOD_REPLY_MARKUP = [['Current📗', 'Week📕']]


def start(bot, update):
    update.message.reply_text(
        'Hi!\nMy name is weatheric. \nIf curious about the weather,\nyou in the right place.' + WINK_EMOJI)


def weather(bot, update):
    update.message.reply_text('Ok!\nFirst of all, send me the name of your city(not implemented) or your geolocation'
                              '.\nTo stop this brunch - /cancel')
    return main.CITY


def city_entered(bot, update, user_data):
    update.message.reply_text('Finally!\nChoose period.\nTo stop this brunch - /cancel',
                              reply_markup=ReplyKeyboardMarkup(WEATHER_PERIOD_REPLY_MARKUP, one_time_keyboard=True))

    user_data[CITY_KEY] = update.message['text']  # provided by tg bot library

    return main.PERIOD


def location_passed(bot, update, user_data):
    user = update.message.from_user
    user_location = update.message.location

    user_data[LONGITUDE_KEY] = str(user_location.longitude)
    user_data[LATITUDE_KEY] = str(user_location.latitude)

    #
    # response = weather_service.get_weather(user_location.latitude, user_location.longitude)
    #
    # update.message.reply_text('Current temp: ' + str(response['main']['temp']) + 'C'
    #                           + '\nWeather: ' + response['weather'][0]['description']
    #                           + '\nExpected temperature: '
    #                           + str(response['main']['temp_min']) + ' - ' + str(response['main']['temp_max'])
    #                           + '\nAtmosphere pressure: ' + str(response['main']['pressure'])
    #                           + '\nWind speed: ' + str(response['wind']['speed']) + 'm/s')

    main.logger.info("Whether request from %s: %f / %f",
                     user.first_name,
                     user_location.latitude,
                     user_location.longitude)

    update.message.reply_text('Finally!\nChoose period.\nTo stop this brunch - /cancel',
                              reply_markup=ReplyKeyboardMarkup(WEATHER_PERIOD_REPLY_MARKUP, one_time_keyboard=True))

    return main.PERIOD


def period_keyboard_pressed(bot, update, user_data):
    response = None

    if CITY_KEY in user_data:
        response = weather_service.get_weather_by_city_name(user_data[CITY_KEY])

        del user_data[CITY_KEY]
    else:
        response = weather_service.get_weather_by_geo(user_data[LATITUDE_KEY], user_data[LONGITUDE_KEY])

        del user_data[LONGITUDE_KEY]
        del user_data[LATITUDE_KEY]

    update.message.reply_text('Current temp: ' + str(response['main']['temp']) + 'C'
                              + '\nWeather: ' + response['weather'][0]['description']
                              + '\nExpected temperature: '
                              + str(response['main']['temp_min']) + ' - ' + str(response['main']['temp_max'])
                              + '\nAtmosphere pressure: ' + str(response['main']['pressure'])
                              + '\nWind speed: ' + str(response['wind']['speed']) + 'm/s',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    main.logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
