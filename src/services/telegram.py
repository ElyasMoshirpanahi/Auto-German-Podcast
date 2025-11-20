import requests
from src.config import BOT_TOKEN, CHANNEL_ID

class TelegramBot:
    def __init__(self):
        if not BOT_TOKEN:
            print("Warning: BOT_TOKEN is not set.")
            self.base_url = None
        else:
            self.base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"

    def send_message(self, text, chat_id=CHANNEL_ID):
        if not self.base_url: return
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        try:
            requests.post(self.base_url + 'sendMessage', data=data)
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_audio(self, file_path, caption=None, chat_id=CHANNEL_ID):
        if not self.base_url: return
        try:
            with open(file_path, 'rb') as f:
                files = {'audio': f}
                data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'HTML'}
                print(f"Sending audio: {file_path}...")
                requests.post(self.base_url + 'sendAudio', files=files, data=data, timeout=300)
        except Exception as e:
            print(f"Error sending audio: {e}")

    def send_photo(self, photo_url, caption=None, chat_id=CHANNEL_ID):
        if not self.base_url: return
        data = {'chat_id': chat_id, 'photo': photo_url, 'caption': caption, 'parse_mode': 'HTML'}
        try:
            requests.post(self.base_url + 'sendPhoto', data=data)
        except Exception as e:
            print(f"Error sending photo: {e}")
