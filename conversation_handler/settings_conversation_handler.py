import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from service import db_service, alert_service, response_service

city_key, alert_key, query_key = 'city', 'alert', 'branch'

cities_keyboard = [[InlineKeyboardButton("Set favorite city", callback_data=city_key)],
                   [InlineKeyboardButton("Set time of alert", callback_data=alert_key)]]


def start(update, context):
    chat_id = update.message.chat_id

    city = db_service.cities[chat_id] if chat_id in db_service.cities else '_none_'

    time = alert_service.alerts[chat_id] if chat_id in alert_service.alerts else '_none_'

    update.message.reply_text('Settings⚙️\n\nFavorite city: ' + city +
                              '\nTime of alert: ' + time,
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=InlineKeyboardMarkup(cities_keyboard))
    from main import category
    return category


def button_clicked(update, context):
    query = update.callback_query

    user_data = context.user_data

    if query.data == city_key:
        context.bot.edit_message_text('Fine!\nNow, please, send me the name of the city.',
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      parse_mode=telegram.ParseMode.MARKDOWN)
        user_data[query_key] = city_key
    else:
        if query.message.chat_id in db_service.cities:
            context.bot.edit_message_text('Fine!\nNow, please, send me time(GMT+3) of alert.'
                                          '\n\nExample: `13:40`'
                                          '\nSend `none` to remove',
                                          chat_id=query.message.chat_id,
                                          message_id=query.message.message_id,
                                          parse_mode=telegram.ParseMode.MARKDOWN)
            user_data[query_key] = alert_key

        else:
            context.bot.edit_message_text('I\'m sorry, but first of all you should add your favorite city🙁',
                                          chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
            return ConversationHandler.END

    from main import data_entered
    return data_entered


def cancel(update, context):
    update.message.reply_text('Bye bye.')
    return ConversationHandler.END


def data_entered(update, context):
    user_data = context.user_data

    if user_data[query_key] == city_key:
        if response_service.is_city_correct(update.message.text):
            update.message.reply_text('Favorite city added')
            db_service.add_city(update.message.chat_id, update.message.text)
        else:
            update.message.reply_text('I can\'t find this city😞')
            from main import data_entered
            return data_entered

        return ConversationHandler.END
    else:
        time = update.message.text

        if time != 'none':
            alert_service.add_alert(time, update.message.chat_id)
            update.message.reply_text('Added!')
        else:
            alert_service.remove_alert(update.message.chat_id)
            update.message.reply_text('Updated!')

    del user_data[query_key]
    return ConversationHandler.END
