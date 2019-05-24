from telegram.ext import ConversationHandler

import main


def help(bot, update):
    update.message.reply_text('List of commands:'
                              '\n\n/add - add favorite city'
                              '\n/weather - show the weather'
                              '\n/predict - weather prediction'
                              '\n/setting - settings')


def cancel(bot, update):
    user = update.message.from_user
    main.logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END
