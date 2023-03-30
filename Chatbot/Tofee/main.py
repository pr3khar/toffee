import logging
from time import time
from datetime import datetime
from telegram.ext import *
from responses import process_message
from pymongo import MongoClient
import re


API_KEY = '6279245879:AAFP_JBtCsXXg1-5MGXQP7cTba4R0uc0K5M'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

names=[]

cluster = MongoClient("mongodb+srv://root:toor@cluster0.8dchtrd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["toffee"]
userCollection = db["users"]
transactionCollection = db["transactions"]

def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. Whats up?')
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    # print(userCollection.find_one())
    count=0
    for x in userCollection.find():
        if(user_id==x.get("username")):
            print("Found")
            count+=1
    print(x)
    if(count==0):
        print("Not found")
        userCollection.insert_one({"username": user_id, "name": user_name})

def help_command(update, context):
    update.message.reply_text('Try typing anything and I will do my best to respond!')

def name_command(update, context):
    names.append(update.message.text)
    logging.info(f'User changed name to {update.message.text}')
    update.message.reply_text(f'User changed name to {update.message.text}')

def handle_messages(update, context):
    update.message.reply_text(f'Please wait. Tracking your budget...')
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    text = str(update.message.text).lower()
    logging.info(f'User ({user_id}) says: {text}')
    amount, category = process_message(text)
    if(category == "food and drink"):
        category="foodAndDrink"
    logging.info(f'Amount: {amount} \tCategory: {category}')

    transactionCollection.insert_one({"amount": amount, "username": user_id, "category": category, "createdAt": int(time())})

    # Bot Response
    update.message.reply_text(f'Amount: {amount} \tCategory: {category}')

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

if __name__== '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('name', name_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_messages))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1)
    updater.idle()