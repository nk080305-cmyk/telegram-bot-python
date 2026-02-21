from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define command handlers

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! This is a simple bot. Type /help for assistance.')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('You can start using the bot by sending /start or /help.')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! How can I assist you today?')


def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot token
    updater = Updater('YOUR_TOKEN')

    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()