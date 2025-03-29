import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetMessagesRequest
from telethon.tl.types import InputMessageID

# Configuration (embedded)
API_ID = 26075878  # Replace with your API ID
API_HASH = "7146213fe4324fcaca1bb6be7a2aef33"  # Replace with your API hash
DELAY = 3600  # Delay in seconds between forwards

async def main():
    # Prompt for the string session
    print("Please enter your phone number (or bot token if using a bot): ")
    phone = input().strip()

    client = TelegramClient("session", API_ID, API_HASH)

    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input("Enter the code received on Telegram: ").strip()
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Enter your 2FA password: ").strip()
            await client.sign_in(password=password)

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
    message = await client(GetMessagesRequest(
        peer=entity,
        id=[InputMessageID(message_id)]
    ))

    if not message.messages:
        print("Message not found.")
        return

    msg_to_forward = message.messages[0]

    # Fetch all groups the user is in
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if d.is_group]

    # Forward to each group
    for group in groups:
        try:
            await client.forward_messages(group.id, msg_to_forward)
            print(f"Forwarded to {group.title}")
            await asyncio.sleep(DELAY)  # Wait before sending to next group
        except Exception as e:
            print(f"Failed to forward to {group.title}: {e}")

    print("Message forwarding complete.")

# Run the script
with TelegramClient("session", API_ID, API_HASH) as client:
    client.loop.run_until_complete(main())
