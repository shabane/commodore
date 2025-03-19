#!/usr/bin/env python3
from telebot_router import TeleBot
import os

app = TeleBot(__name__)


@app.route('/command ?(.*)')
def helper(message, cmd):
    chat_dest = message['chat']['id']
    app.send_message(chat_dest, "fuck")


if __name__ == '__main__':
    app.config['api_key'] = os.environ.get('API_KEY')
    app.poll(debug=True)
