import requests
import os


class TelegramClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.api_url = f'https://api.telegram.org/bot{api_token}/'

    def sendPhoto(self, path: str, chat_id: str):
        if not os.path.exists(path):
            raise FileExistsError(f'no such file: {path}')

        with open(path, 'rb') as fli:
            res = requests.post(os.path.join(self.api_url, 'sendPhoto'), data={'chat_id': chat_id}, files={'photo': fli})
            return res.json()
