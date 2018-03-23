from flask import Flask
from flask import request
import config
import json
import utils
import texts

import telegram

from objs.LeftChatMember import LeftChatMember

bot = telegram.Bot(token=config.cryptoShook_bot_token)

app = Flask(__name__)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_new_chat_member(message_json):
    try:
        new_chat_member = message_json['message']['new_chat_member']
        print('new_chat_member: {}'.format(new_chat_member))
    except Exception:
        print('NO new_chat_member')
    pass


def handle_left_member(message_json):
    uid = message_json['message']['left_chat_member']['id']
    first_name = str(message_json['message']['left_chat_member']['first_name'])
    last_name = str(message_json['message']['left_chat_member']['last_name'])
    date = message_json['message']['date']

    try:
        username = str(message_json['message']['left_chat_member']['username'])
        print('username: {}'.format(username))
    except Exception:
        print('---Exception--- cant get username!')

    left_member = LeftChatMember(uid, first_name, last_name, date)

    left_members = utils.load_left_members()
    left_members[uid] = left_member
    utils.save_left_members(left_members)
    pass


def new_member_greeting(message_json):
    chat_id = message_json['message']['chat']['id']
    new_chat_member = message_json['message']['new_chat_member']
    message_id = message_json['message']['message_id']
    uid = new_chat_member['id']
    name = '{} {}'.format(new_chat_member['first_name'], new_chat_member['last_name'])

    if utils.is_new_user(uid):
        bot.send_message(chat_id, 'Hello {}'.format(name), reply_to_message_id=message_id)
    else:
        bot.send_message(chat_id, 'Welcome back {}'.format(name), reply_to_message_id=message_id)

    pass


def handle_new_message(message_json):
    chat_id = message_json['message']['chat']['id']
    message_id = message_json['message']['message_id']

    bot.send_message(chat_id, texts.msg_welcome)

    pass


def process_from_chat(message_json):
    new_chat_member = utils.get_new_chat_member(message_json)
    left_chat_member = utils.get_left_chat_member(message_json)

    message = utils.get_message(message_json)

    if new_chat_member:
        new_member_greeting(message_json)
    if left_chat_member:
        handle_left_member(message_json)
    if message:
        handle_new_message(message_json)
        print('new message: \n{}'.format(message))
    pass


# _________________________________(◑‿◐)_______________________________________________________


def process_new_message(message_json):
    print('process_new_message')
    chat_id = str(message_json['message']['chat']['id'])

    if chat_id == config.CHAT_ID:
        process_from_chat(message_json)
    else:
        bot.send_message(chat_id, 'Hi)\ncan`t talk to you yet\nSorry...')
        print('Message not from CryptoShook chat !!!')

    pass


# _________________________________◦°˚\(*❛‿❛)/˚°◦_______________________________________________________


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_request = request.get_json()
        write_json(json_request, 'msgs.message_{}'.format(json_request['update_id']))
        print('new message json:\n{}\n'.format(json_request))

        process_new_message(json_request)

    return '<h1>Hi there</h1>'


# _________________________________(´◉◞౪◟◉｀)_______________________________________________________


if __name__ == "__main__":
    app.run(debug=True)

# _________________________________(◕‿‿◕｡)_______________________________________________________
