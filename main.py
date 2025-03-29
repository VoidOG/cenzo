import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

# Configuration
API_ID = 26075878  # Replace with your API ID
API_HASH = "7146213fe4324fcaca1bb6be7a2aef33"  # Replace with your API hash
DELAY = 3600  # Delay in seconds between forwards

# Ask for the Telethon string session
SESSION_STRING = input("Enter your Telethon string session: ").strip()

async def main():
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        print("Logged in successfully!")

        # Ask for the message link
        message_link = input("Enter the Telegram message link: ").strip()

        # Extract chat ID and message ID from the link
        try:
            parts = message_link.split('/')
            chat_username = parts[-2]
            message_id = int(parts[-1])
        except (IndexError, ValueError):
            print("Invalid message link format.")
            return

        # Get the entity (chat) from the username or ID
        entity = await client.get_entity(chat_username)

        # Fetch the message
        message = await client.get_messages(entity, ids=message_id)

        if not message:
            print("Message not found.")
            return

        # Fetch all groups the account is in
        dialogs = await client.get_dialogs()
        groups = [d for d in dialogs if d.is_group]

        # Forward to each group
        for group in groups:
            try:
                await client.forward_messages(group.id, message)
                print(f"Forwarded to {group.title}")
                await asyncio.sleep(DELAY)  # Wait before sending to next group
            except Exception as e:
                print(f"Failed to forward to {group.title}: {e}")

        print("Message forwarding complete.")

# Run the script
asyncio.run(main())
