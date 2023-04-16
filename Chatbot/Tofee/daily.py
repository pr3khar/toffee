import schedule
from pymongo import MongoClient
import requests
import time

API_KEY = '6279245879:AAFP_JBtCsXXg1-5MGXQP7cTba4R0uc0K5M'

cluster = MongoClient("mongodb+srv://root:toor@cluster0.8dchtrd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["toffee"]
userCollection = db["users"]
transactionCollection = db["transactions"]
ids=[]

def daily_message():
    print("Started Daily\n")
    reply_no = "No money spent today"
    reply=""
    for id in ids:
        transactions = transactionCollection.find({"username": id["user_id"]})
        if(transactions.count()==0):
            reply = reply_no
            print(reply)
        for t in transactions:
            print(t)
            print("\n")
        data = {
            "chat_id": id["chat_id"],
            "text": reply
        }
        url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"


schedule.every().day.at('20:54').do(daily_message)

while True:
    schedule.run_pending()
    print("Waiting...")
    time.sleep(6)