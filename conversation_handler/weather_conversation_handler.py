import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

import main
from service import callback_service, db_service, response_service

latitude_key, longitude_key, city_key = 'lat', 'lon', 'city'

periods_keyboard = [[InlineKeyboardButton("Current", callback_data='1'),
                     InlineKeyboardButton("Full day", callback_data='2')],
                    [InlineKeyboardButton("5 days", callback_data='3')]]

start_message = '*Great!*\nFirst of all, send me the name ' \
                        'of city or geolocation. Also you can add favourite city from settings. ' \
                        '\n\n_To stop this branch -_ /cancel'

periods_message = '*Finally!*\nChoose period.\n\n_To stop this branch -_ /cancel'


def start(update, context):
    if update.message.chat_id in db_service.cities:
        city = db_service.cities[update.message.chat_id]
        inline = [[InlineKeyboardButton(city, callback_data=update.message.chat_id)]]

        update.message.reply_text(start_message,
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=InlineKeyboardMarkup(inline))

    else:
        update.message.reply_text(start_message,
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    return main.category


def city_branch(update, context):
    user_data = context.user_data

    update.message.reply_text(periods_message,
                              reply_markup=InlineKeyboardMarkup(periods_keyboard),
                              parse_mode=telegram.ParseMode.MARKDOWN)

    user_data[city_key] = update.message.text

    return main.data_entered


def location_branch(update, context):
    user_data = context.user_data

    user = update.message.from_user
    user_location = update.message.location

    user_data[longitude_key] = str(user_location.longitude)
    user_data[latitude_key] = str(user_location.latitude)

    main.logger.info("Whether request from %s: %f / %f",
                     user.first_name,
                     user_location.latitude,
                     user_location.longitude)

    update.message.reply_text(periods_message,
                              reply_markup=InlineKeyboardMarkup(periods_keyboard),
                              parse_mode=telegram.ParseMode.MARKDOWN)

    return main.period


def period_entered(update, context):
    user_data = context.user_data

    query = update.callback_query

    context.bot.send_chat_action(chat_id=query.message.chat_id, action=telegram.ChatAction.TYPING)

    id = query.data

    if city_key in user_data:
        response = response_service.weather_by_city_name(id, user_data[city_key])
        del user_data[city_key]

    else:
        response = response_service.weather_by_geolocation(id, user_data[latitude_key], user_data[longitude_key])

        del user_data[longitude_key]
        del user_data[latitude_key]

    if '404' != response['cod']:
        context.bot.edit_message_text(callback_service.get_weather(id, response),
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.edit_message_text('I can\'t find this city🙁\n\nPlease, if the name of '
                                      'the city is correct, call my developer @Anrix_official',
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id)

    return ConversationHandler.END


def period(bot, update):
    update.message.reply_text('*Finally!*\nChoose period.\n\n_To stop this branch -_ /cancel',
                              reply_markup=InlineKeyboardMarkup(periods_keyboard),
                              parse_mode=telegram.ParseMode.MARKDOWN)


def favorite_city_branch(update, context):
    query = update.callback_query

    user_data = context.user_data

    key = int(query.data)
    user_data[city_key] = db_service.cities[key]

    context.bot.edit_message_text(periods_message,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=InlineKeyboardMarkup(periods_keyboard))

    return main.period
