import logging
from telegram.ext import *
import responses

API_KEY = '6279245879:AAFP_JBtCsXXg1-5MGXQP7cTba4R0uc0K5M'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. Whats up?')

def help_command(update, context):
    update.message.reply_text('Try typing anything and I will do my best to respond!')

def custom_command(update, context):
    update.message.reply_text('This is a custom command ')

def handdle_messages(update, context):
    text = str(update.message.text).lower()
    logging.info('f!User ({update.message.chat.id}) says: {text}')

    # Bot Response
    update.message.reply_text(text)

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

if __name__== '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handdle_messages))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1)
    updater.idle()