import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
MONGODB_URI = os.getenv('MONGODB_URI')
TMP_DIR = os.getenv('TMP_DIR', 'tmp')
