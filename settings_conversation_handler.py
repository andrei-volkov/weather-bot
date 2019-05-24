from datetime import datetime, date, time

import schedule as schedule
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

import db_service
import output_service
import response_service

CITY_KEYBOARD = [[InlineKeyboardButton("Set favourite city", callback_data='1')],
                 [InlineKeyboardButton("Set time of alert", callback_data='2')]]

QUERY_RES_KEY = 'branch'


def settings(update, context):
    user_data = context.user_data
    chat_id = update.message.chat_id

    city = db_service.users_cities[chat_id] if chat_id in db_service.users_cities \
        else '_none_'

    time = user_data[chat_id] if chat_id in user_data else '_none_'

    update.message.reply_text('Settings⚙️\n\nFavourite city: ' + city +
                              '\nTime of alert: ' + time,
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=InlineKeyboardMarkup(CITY_KEYBOARD))
    from main import ENTER_CITY
    return ENTER_CITY


def button_clicked(update, context):
    query = update.callback_query

    user_data = context.user_data

    if query.data == '1':
        context.bot.edit_message_text('Fine!\nNow, please, send me the name of the city.',
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      parse_mode=telegram.ParseMode.MARKDOWN)
        user_data[QUERY_RES_KEY] = '1'
    else:
        if query.message.chat_id in db_service.users_cities:
            context.bot.edit_message_text('Fine!\nNow, please, send me time(GMT+3) of alert.'
                                          '\n\nExample: `13:40`',
                                          chat_id=query.message.chat_id,
                                          message_id=query.message.message_id,
                                          parse_mode=telegram.ParseMode.MARKDOWN)
            user_data[QUERY_RES_KEY] = '2'
        else:
            context.bot.edit_message_text('I\'m sorry, but first of all you should add your favourite city🙁',
                                          chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
            return ConversationHandler.END

    from main import CITY_ENTERED
    return CITY_ENTERED


def cancel(update, context):
    update.message.reply_text('Bye bye.')
    return ConversationHandler.END


def data_entered(update, context):
    user_data = context.user_data

    if user_data['branch'] == 1:
        if response_service.is_city_correct(update.message.text):
            update.message.reply_text('Favourite city added')
            db_service.add_city(update.message.chat_id, update.message.text)
        else:
            update.message.reply_text('I can\'t find this city😞')
            from main import CITY_ENTERED
            return CITY_ENTERED

        return ConversationHandler.END
    else:
        time = update.message.text
        schedule.every().day.at(time).do(alert, context, update.message.chat_id)


    return ConversationHandler.END
    del user_data[QUERY_RES_KEY]


def alert(context, chat_id):
    response = response_service.get_by_query_name(1, db_service.users_cities[chat_id])
    res = output_service.output_by_id(1, response)

    print('test')
    context.bot.send_message(chat_id, text=res, parse_mode=telegram.ParseMode.MARKDOWN)
