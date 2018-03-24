from flask import Flask
from flask import request

import config

import telegram

import utils

bot = telegram.Bot(token=config.cryptoShook_news_bot_token)

app = Flask(__name__)


# _________________________________(◑‿◐)_______________________________________________________


def process_new_message(message_json):
    print('process_new_message')
    chat_id = utils.get_chat_id(message_json)

    if chat_id == config.CryptoShookMaster_ID:

        message = utils.get_message(message_json)
        print('message: {}'.format(message))

        bot.send_message(config.CryptoShook_News_ID, message, parse_mode=telegram.ParseMode.MARKDOWN)

    pass


# _________________________________◦°˚\(*❛‿❛)/˚°◦_______________________________________________________


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        json_request = request.get_json()
        print('new message json:\n{}\n'.format(json_request))
        utils.write_json(json_request, 'msgs.message_{}'.format(json_request['update_id']))

        try:
            process_new_message(json_request)
        except Exception:
            # TODO create Exception object (◕‿‿◕｡)
            return None

    return '<h1>Hi there</h1>'


# _________________________________(´◉◞౪◟◉｀)_______________________________________________________


if __name__ == "__main__":
    app.run(debug=True)

# _________________________________(◕‿‿◕｡)_______________________________________________________
