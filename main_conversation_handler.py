from telegram.ext import ConversationHandler

import main

WINK_EMOJI = u"\U0001F609"


def start(update, context):
    update.message.reply_text('Hi!\nMy name is weatheric. \nIf curious about the weather,'
                              '\nyou in the right place😉' + WINK_EMOJI)


def help(update, context):
    update.message.reply_text('List of commands:'
                              '\n\n/add - add favorite city'
                              '\n/weather - show the weather'
                              '\n/predict - weather prediction'
                              '\n/setting - settings')


def cancel(update, context):
    user = update.message.from_user
    main.logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END
