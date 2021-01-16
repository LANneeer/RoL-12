import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

PG_USER = str(os.getenv("PG_USER"))
PG_PASSWORD = str(os.getenv("PG_PASSWORD"))

IP = os.getenv("IP")

I18N_DOMAIN = 'ROL'

BASE_DIR = Path(__file__).parents[1]

LOCALES_DIR = BASE_DIR / 'locales'

admins = []
