#!/usr/bin/env python3
from telebot_router import TeleBot
import os
import yaml
from telsdk import TelegramClient

app = TeleBot(__name__)
telegram_client = TelegramClient(os.environ.get('API_KEY'))

prompts = None
with open(f'{os.environ.get("PROMPTS_FILE", "./prompts.yaml")}', 'r') as fle:
    prompts = yaml.safe_load(fle)

@app.route('/ ?(.*)')
def menu(message, cmd):
    chat_dest = message['chat']['id']
    for prompt in prompts.get('commands'):
        if prompt.get('key') == cmd:
            app.send_message(chat_dest, f'{prompt.get("message")}') if prompt.get("message") else ...

            if prompt.get('photos'):
                for photo in prompt.get('photos'):
                    telegram_client.sendPhoto(photo, chat_dest)

            if prompt.get('audios'):
                for audio in prompt.get('audios'):
                    telegram_client.sendAudio(audio, chat_dest)

            return
    app.send_message(chat_dest, f'دستور اشتباه است!')


if __name__ == '__main__':
    app.config['api_key'] = os.environ.get('API_KEY')
    app.poll(debug=True)
