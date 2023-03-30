import re
from model import classify_text

def process_message(message):
    list_message = message.lower().split()
    print(list_message)
    if(len(list_message)<1):
        return[-1, "No_Message"]
    
    amount = list_message[0]
    if(len(list_message)==1):
        if(amount.isnumeric()):
            return [int(amount), 'Misc']
        else:
            return[-1, "Not_A_Number"]
    
    if(amount.isnumeric()):
        return [int(amount), classify_text(list_message[1])]
    else:
        for x in list_message:
            if(x.isnumeric()):
                return [int(x), classify_text(list_message[0])]
    return[-1, "Not_A_Number"]
        
    
    
    
