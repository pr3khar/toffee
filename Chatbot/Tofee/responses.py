import regex

def process_message(message, response_array, response):
    list_message = re.findall(r"[w']+|[.,!?;]", message.lower())

    score = 0
    for word in list_message:
        if(word in response_array):
            score = score + 1

    print(score, response)
    return [score, response]

def get_response(message):
    response_list = [
        process_message(message, ['hello', 'hi', 'hey'], 'Hey there!')
        
    ]