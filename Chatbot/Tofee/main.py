# -*- coding: utf-8 -*-
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
help_message = "Hello and welcome to Toffee, your go-to budget management platform! We're thrilled to have you here and excited to help you take control of your finances.\n\nWith Toffee, you can easily keep track of your expenses and stick to your budget. Adding a transaction is simple - just enter the amount and the type of transaction. You can do this by typing the number followed by the type or the type followed by the number, separated by a space. For example, you could enter \"10 coffee\", \"groceries 50\" or just \"20\".\n\nWe're here to support you every step of the way, so if you have any questions or need help getting started, just let us know.\nYour budget is expanded on further on \ntoffee.azurewebsites.net/"
hindi_help_message = "नमस्कार और टॉफ़ी में आपका स्वागत है, आपका पसंदीदा बजट प्रबंधन मंच! हम आपको यहां पाकर रोमांचित हैं और आपके वित्त को नियंत्रित करने में आपकी मदद करने के लिए उत्साहित हैं।\nटॉफ़ी के साथ, आप आसानी से अपने खर्चों पर नज़र रख सकते हैं और अपने बजट पर टिके रह सकते हैं। लेन-देन जोड़ना सरल है - बस राशि और लेन-देन का प्रकार दर्ज करें। आप टाइप के बाद संख्या टाइप करके या स्पेस द्वारा अलग किए गए नंबर के बाद टाइप टाइप करके ऐसा कर सकते हैं। उदाहरण के लिए, आप \"10 कॉफ़ी\", \"किराने का सामान 50\" या केवल \"20\" दर्ज कर सकते हैं।\nहम यहां हर कदम पर आपका समर्थन करने के लिए हैं, इसलिए यदि आपके कोई प्रश्न हैं या आरंभ करने में सहायता की आवश्यकता है, तो बस हमें बताएं।\nआपका बजट toffee.azurewebsites.net/"

cluster = MongoClient("mongodb+srv://root:toor@cluster0.8dchtrd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["toffee"]
userCollection = db["users"]
transactionCollection = db["transactions"]
ids=[]
chatidsss=[]
isHindi = False

def start_command(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_name = str(user_name)
    chatid = update.message.chat_id
    # print(userCollection.find_one())
    count=0
    x=userCollection.find_one({"username":str(user_id)})
    # print(x)
    
    for x in userCollection.find():
        # print(x)
        if(str(user_id)==x["username"]):
            print("Found")
            count+=1
            if(isHindi):
                update.message.reply_text(f'उपयोगकर्ता पहले मिला! वापसी पर स्वागत है {user_name}!!')
            else:
                update.message.reply_text(f'User found previously! Welcome back {user_name}!!')
    # print(x)
    if(count==0):
        print("Not found")
        userCollection.insert_one({"username": str(user_id), "name": str(user_name), "chatID": str(chatid)})
        if(isHindi):
            update.message.reply_text(f'नमस्कार {user_name}, आप हमारे साथ जुड़कर बहुत अच्छा लगा!')
        else:
            update.message.reply_text(f'Hello {user_name}, great to have you join us!')
    
    if(isHindi):
        update.message.reply_text(hindi_help_message+str(user_id)+"पर आगे बढ़ाया गया है\nखुश बजट!")
    else:
        update.message.reply_text(help_message+str(user_id)+"\nHappy budgeting!")

    if(chatid not in chatidsss):
        chatidsss.append(chatid)
        ids.append({"chat_id": chatid, "user_id":user_id})
    
    # data = {
    #     "chat_id": chatid,
    #     "text": "Hello"
    # }
    # url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"

    # response = requests.post(url, data=data)

    # # Check the response status code
    # if response.status_code == 200:
    #     print("Message sent successfully!")
    # else:
    #     print("Failed to send message.")
    
    # daily_message()

def help_command(update, context):
    if(isHindi):
        update.message.reply_text(hindi_help_message+str(user_id)+"पर आगे बढ़ाया गया है\nखुश बजट!")
    else:
        update.message.reply_text(help_message+str(user_id)+"\nHappy budgeting!")

def handle_messages(update , context):
    if(isHindi):
        update.message.reply_text(f'कृपया प्रतीक्षा करें। हम आपका बजट ट्रैक कर रहे हैं...')
    else:
        update.message.reply_text(f'Please wait. Tracking your budget...')
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    text = str(update.message.text).lower()
    logging.info(f'User ({user_id}) says: {text}')
    amount, category, msg = process_message(text)
    if(category == "food and drink"):
        category="foodAndDrink"
    if(amount==-1):
        if(isHindi):
            update.message.reply_text(f'माफ़ करें, मैं समझ नहीं पाया। क्या आप इसे दोबारा कह सकते हैं?')
        else:
            update.message.reply_text(f'Sorry, I didn\'t catch that could you rephrase it.')
        return
    logging.info(f'Amount: {amount} \tCategory: {category}')

    transactionCollection.insert_one({"amount": amount, "username": str(user_id), "category": str(category), "createdAt": int(time()), "message": str(msg)})
    if(isHindi):
        update.message.reply_text(f'लेन-देन जोड़ा गया!!\nराशि: {amount} \tवर्ग: {category}')
    else:
        update.message.reply_text(f'Transaction added!!\nAmount: {amount} \tCategory: {category}')

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

def english(update, context):
    isHindi = False

def hindi(update, context):
    print("Changed")
    isHindi = True

if __name__== '__main__':
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('english', english))
    dp.add_handler(CommandHandler('hindi', hindi))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_messages))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1)
    updater.idle()