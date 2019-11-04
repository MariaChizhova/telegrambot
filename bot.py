import json

import requests
import logging
import emoji

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')

logger = logging.getLogger()

with open('token.txt', 'r') as f:
    TOKEN = json.load(f)['token']

GET_UPDATES = "getUpdates"
SEND_MESSAGE = "sendMessage"


def send_request(method_name, params={}):
    url = "https://api.telegram.org/bot{}/".format(TOKEN) + method_name
    response = requests.get(url, params)
    content = json.loads(response.content.decode("utf8"))
    if not content['ok']:
        raise RuntimeError(url, content)
    return content


def get_updates(update_id):
    params = {'allowed_updates': 'message',
              'timeout': 10}  # Allows to use long polling
    if update_id is not None:
        params['offset'] = update_id
    response = send_request(GET_UPDATES, params)
    return response['result']


def send_message(text, chat_id):
    logger.info(f"Answered to {chat_id}")
    try:
        send_request(SEND_MESSAGE, params={"text": text,
                                           "chat_id": chat_id})
    except:
        logger.info(f"Couldn't send a message to user {chat_id}")


def get_id_by_name(name, surname):
    with open("names.txt", 'r') as f:
        data = f.read().split()
        students = {data[i]: int(data[i + 1]) for i in range(0, len(data), 2)}
    try:
        return students[name + surname]
    except KeyError:
        return None


def process_new_message(message):
    print(message)
    message = message["message"]
    chat_id = message["chat"]["id"]
    text = message["text"]
    text = text.lower()

    if 'entities' in message and message['entities'][0]['type'] == 'bot_command':
        if text == '/start':
            send_message("Привет! Введи имя и фамилию.", chat_id)
        else:
            send_message("Я тебя не понимаю.", chat_id)
    else:
        print(text)
        try:
            name, surname = text.split()
        except:
            send_message("Неправильный формат ввода.", chat_id)
        else:
            student_id = get_id_by_name(name, surname)
            student_rev_id = get_id_by_name(surname, name)
            if (student_id or student_rev_id):
                send_message("https://github.com/Glebanister/AMIS_GUYS_bot/blob/master/images/image{}.jpg".format(student_id if student_id else student_rev_id), chat_id)
            else:
                send_message("https://github.com/Glebanister/AMIS_GUYS_bot/blob/master/images/F.gif", chat_id)

