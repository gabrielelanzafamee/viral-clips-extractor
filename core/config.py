import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN', None)
COOKIES_TIKTOK_PATH = "cookies.txt"