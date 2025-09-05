import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

PREFIX = os.getenv('PREFIX')

if not DISCORD_TOKEN:
    print("Warning: DISCORD_TOKEN is not set.")
else:
    print("DISCORD_TOKEN loaded successfully.")


if not PREFIX:
    print("warning: PREFIX IS NOT SET.")
else:
    print("PREFIX loaded successfully.")