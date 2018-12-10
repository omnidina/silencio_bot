# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from threading import Timer
import logging

users_countdown = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Say no more. I'm on it!")


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text("God help those who help themselves.")


def delete_message(bot, update):
    """Delete the user's message which is sent more than one time per hour."""
    user_id = update.message.from_user.id
    if user_id not in users_countdown.keys():
        users_countdown[user_id] = 'Blocked'
        timer = Timer(3600, stop_timer_for_user, [user_id])
        timer.start()
    else:
        bot.send_message(update.message.chat_id,
                         f'Too many voice messages. Try later, {update.message.from_user.username}')
        update.message.delete()


def stop_timer_for_user(user_id):
    del users_countdown[user_id]


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on  non-command - e.g delete message in Telegram
    dp.add_handler(MessageHandler(Filters.voice, delete_message))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
