import logging
from time import time
from datetime import datetime
from telegram.ext import *
import requests
from responses import process_message
from pymongo import MongoClient
import re


API_KEY = '6279245879:AAFP_JBtCsXXg1-5MGXQP7cTba4R0uc0K5M'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

names=[]
help_message = "Hello and welcome to Toffee, your go-to budget management platform! We're thrilled to have you here and excited to help you take control of your finances.\n\nWith Toffee, you can easily keep track of your expenses and stick to your budget. Adding a transaction is simple - just enter the amount and the type of transaction. You can do this by typing the number followed by the type or the type followed by the number, separated by a space. For example, you could enter \"10 coffee\", \"groceries 50\" or just \"20\".\n\nWe're here to support you every step of the way, so if you have any questions or need help getting started, just let us know. Happy budgeting!"

cluster = MongoClient("mongodb+srv://root:toor@cluster0.8dchtrd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["toffee"]
userCollection = db["users"]
transactionCollection = db["transactions"]
ids=[]

def start_command(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_name = str(user_name)
    # print(userCollection.find_one())
    count=0
    for x in userCollection.find():
        if(user_id==x.get("username")):
            print("Found")
            count+=1
            update.message.reply_text(f'User found previously! Welcome back {user_name}!!')
    # print(x)
    if(count==0):
        print("Not found")
        userCollection.insert_one({"username": user_id, "name": user_name})
        update.message.reply_text(f'Hello {user_name}, great to have you join us!')
    update.message.reply_text(help_message)
    chatid = update.message.chat_id
    if(chatid not in ids):
        ids.append({"chat_id": chatid, "user_id":user_id})
    
    data = {
        "chat_id": chatid,
        "text": "Hello"
    }
    url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"

    response = requests.post(url, data=data)

    # Check the response status code
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")
    
    # daily_message()

def help_command(update, context):
    update.message.reply_text(help_message)

def name_command(update, context):
    names.append(update.message.text)
    logging.info(f'User changed name to {update.message.text}')
    update.message.reply_text(f'User changed name to {update.message.text}')

def handle_messages(update , context):
    update.message.reply_text(f'Please wait. Tracking your budget...')
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    text = str(update.message.text).lower()
    logging.info(f'User ({user_id}) says: {text}')
    amount, category = process_message(text)
    if(category == "food and drink"):
        category="foodAndDrink"
    if(amount==-1):
        update.message.reply_text(f'Sorry, I didn\'t catch that could you rephrase it.')
        return
    logging.info(f'Amount: {amount} \tCategory: {category}')

    transactionCollection.insert_one({"amount": amount, "username": user_id, "category": category, "createdAt": int(time())})
    update.message.reply_text(f'Transaction added!!\nAmount: {amount} \tCategory: {category}')

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