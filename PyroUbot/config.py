import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "200"))

DEVS = list(map(int, os.getenv("DEVS", "7575136006").split()))

API_ID = int(os.getenv("API_ID", "31277058"))

API_HASH = os.getenv("API_HASH", "8b59f544f0a85a8b1d00b6fb531f6e33")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8355020103:AAG6hM05quhF6boAt8pvJeekZFNaTH8bK14")

OWNER_ID = int(os.getenv("OWNER_ID", "7575136006"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002344868631").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://fahrezaaofa99_db_user:MaDxG0QrTb8zWBIq@cluster0.hbn1ayd.mongodb.net/?appName=Cluster0")

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1003868561588"))
