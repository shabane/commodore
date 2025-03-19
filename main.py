#!/usr/bin/env python3
from telebot_router import TeleBot
import os
import yaml

app = TeleBot(__name__)

prompts = None
with open(f'{os.environ.get("PROMPTS_FILE", "./prompts.yaml")}', 'r') as fle:
    prompts = yaml.safe_load(fle)

print(prompts)

@app.route('/command ?(.*)')
def helper(message, cmd):
    chat_dest = message['chat']['id']
    app.send_message(chat_dest, "fuck")


if __name__ == '__main__':
    app.config['api_key'] = os.environ.get('API_KEY')
    app.poll(debug=True)
