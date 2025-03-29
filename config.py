import os

API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING", "YOUR_SESSION_STRING")  # Telethon string session

DELAY = int(os.getenv("DELAY", "3600"))  # Delay (in seconds) between forwards
