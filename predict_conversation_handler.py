import telegram

from telegram.ext import ConversationHandler

import predictor_service

INFO_MESSAGE = 'Please send me list of some params:' \
               '\n- Min temp 1 day ago' \
               '\n- Min temp 2 days ago' \
               '\n- Min temp 3 days ago' \
               '\n- Max dew Point 1 day ago(°C)' \
               '\n- Max dew Point 3 day ago(°C)' \
               '\n- Min dew Point 1 day ago(°C)' \
               '\n- Max temp 1 day ago' \
               '\n\nExample: `8 11 12 14 13 7 20`' \
               '\nBe careful, the *sequence* is important.'

EROR_MESSAGE = 'Incorrect data'
AVERAGE_TEMP = 'Average temp today will be: '


def predict(update, context):
    update.message.reply_text(INFO_MESSAGE,
                              parse_mode=telegram.ParseMode.MARKDOWN)

    import main
    return main.PREDICT_DATA_ENTERED


def get_predict(update, context):
    data = update.message.text.split(' ')

    if len(data) != 7:
        update.message.reply_text(EROR_MESSAGE,
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        data_int = list(map(int, data))
        data_int.insert(0, 1)

        temp = round(predictor_service.get_predict(data_int), 2)

        update.message.reply_text(AVERAGE_TEMP
                                  + str(temp) + '(°C)',
                                  parse_mode=telegram.ParseMode.MARKDOWN)

    return ConversationHandler.END
