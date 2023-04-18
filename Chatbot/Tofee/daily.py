import schedule
from pymongo import MongoClient
import requests
from time import time

API_KEY = '6279245879:AAFP_JBtCsXXg1-5MGXQP7cTba4R0uc0K5M'

cluster = MongoClient("mongodb+srv://root:toor@cluster0.8dchtrd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["toffee"]
userCollection = db["users"]
transactionCollection = db["transactions"]
hindi_text = u'\u0928\u092e\u0938\u094d\u0924\u0947'
print(hindi_text)
isHindi = False
ids=[]
for x in userCollection.find():
    # print(x)
    ids.append(x)

print(ids)

def daily_message():
    print("Started Daily\n")
    reply_no = "No money spent today"
    reply=""
    for id in ids:
        labels = ["entertainment", "food and drink", "home", "lifestyle", "transportation", "utilities", "Miscellaneous"]
        costs=[0, 0, 0, 0, 0, 0, 0]
        transactions = transactionCollection.find({"username": id["username"]})
        print(transactions)
            # reply = reply_no
            # print(reply)
        count=0
        for t in transactions:
            # print(int(time())-t["createdAt"])
            if(int(time())-t["createdAt"] < 86400):
                c = t["category"]
                if(c in labels):
                    i=0
                    for l in labels:
                        if(l==c):
                            costs[i]+=int(t["amount"])
                        i+=1
                # reply+=f'{t["category"]} : {t["amount"]}\n'
                # print("\n")
                count+=1
        reply='Todays Transactions: \n'
        i=0
        for x in labels:
            reply+=f'{x}: {costs[i]}\n'
            i+=1
        if(count==0):
            reply=reply_no
        print(reply)
        data = {
            "chat_id": id["chatID"],
            "text": reply
        }

        url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"

        response = requests.post(url, data=data)

        # Check the response status code
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Failed to send message.")


schedule.every().day.at("00:00").do(daily_message)

daily_message()
# while True:
#     schedule.run_pending()
#     print("Waiting...")
#     time.sleep(6)