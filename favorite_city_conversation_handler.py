from telegram.ext import ConversationHandler

from main import logger, NOT_IMPLEMENTED


def add(bot, update):
    update.message.reply_text('This feature is not implemented.')
    return NOT_IMPLEMENTED


def cancel(bot, update):
    update.message.reply_text('Bye bye.')
    return ConversationHandler.END
