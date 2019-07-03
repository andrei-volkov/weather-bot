import telegram

from telegram.ext import ConversationHandler

from service import predictor_service

error_message = 'Incorrect data'
result_message = 'Average temp today will be: '
predictor_params_message = 'Please send me list of some params:' \
                           '\n- Min temp 1 day ago' \
                           '\n- Min temp 2 days ago' \
                           '\n- Min temp 3 days ago' \
                           '\n- Max dew point 1 day ago(°C)' \
                           '\n- Max dew point 3 day ago(°C)' \
                           '\n- Min dew point 1 day ago(°C)' \
                           '\n- Max temp 1 day ago' \
                           '\n\nExample: `8 11 12 14 13 7 20`' \
                           '\nBe careful, the *sequence* is important.'


def start(update, context):
    update.message.reply_text(predictor_params_message, parse_mode=telegram.ParseMode.MARKDOWN)

    import main
    return main.prediction_params_entered


def prediction(update, context):
    data = update.message.text.split(' ')

    if len(data) != 7:
        update.message.reply_text(error_message, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        data_int = list(map(int, data))
        data_int.insert(0, 1)

        temp = round(predictor_service.get_prediction(data_int), 2)

        update.message.reply_text(result_message + str(temp) + '(°C)', parse_mode=telegram.ParseMode.MARKDOWN)

    return ConversationHandler.END
