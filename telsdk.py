import requests
import os


class TelegramClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.api_url = f'https://api.telegram.org/bot{api_token}/'

    def sendPhoto(self, path: str, chat_id: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f'no such file: {path}')

        with open(path, 'rb') as fli:
            res = requests.post(os.path.join(self.api_url, 'sendPhoto'), data={'chat_id': chat_id}, files={'photo': fli})
            return res.json()

    def sendAudio(self, path: str, chat_id: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f'no such file: {path}')

        with open(path, 'rb') as fli:
            res = requests.post(os.path.join(self.api_url, 'sendAudio'), data={'chat_id': chat_id}, files={'audio': fli})
            return res.json()

    def sendDocument(self, path: str, chat_id: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f'no such file: {path}')

        with open(path, 'rb') as fli:
            res = requests.post(os.path.join(self.api_url, 'sendDocument'), data={'chat_id': chat_id}, files={'document': fli})
            return res.json()

    def sendVideo(self, path: str, chat_id: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f'no such file: {path}')

        if os.stat(path).st_size * 2 ** 20 >= 50:
            raise Exception('video too big. it should be under 50MB')

        with open(path, 'rb') as fli:
            res = requests.post(os.path.join(self.api_url, 'sendVideo'), data={'chat_id': chat_id}, files={'video': fli})
            return res.json()
