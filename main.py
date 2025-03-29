from telethon import TelegramClient
import asyncio
import config
import re

# Initialize Telethon client
client = TelegramClient("session", config.API_ID, config.API_HASH)

async def get_user_groups():
    """Fetch groups where the bot is present."""
    groups = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            groups.append(dialog.entity.id)
    return groups

async def forward_message(message_link):
    """Extracts message details and forwards to groups."""
    match = re.search(r"https://t.me/([^/]+)/(\d+)", message_link)
    if not match:
        print("Invalid link! Please provide a valid Telegram message link.")
        return
    
    username_or_id, message_id = match.groups()
    message_id = int(message_id)

    try:
        entity = await client.get_entity(username_or_id)  # Get chat ID
        chat_id = entity.id
    except Exception as e:
        print(f"Error fetching chat ID: {e}")
        return

    groups = await get_user_groups()
    if not groups:
        print("Bot is not in any groups.")
        return

    for group_id in groups:
        try:
            await client.forward_messages(group_id, message_id, chat_id)
            print(f"Forwarded to {group_id}")
            await asyncio.sleep(config.DELAY)
        except Exception as e:
            print(f"Failed to forward to {group_id}: {e}")

async def main():
    """Main function to get user input and forward messages."""
    await client.start()
    message_link = input("Enter the Telegram message link: ")
    await forward_message(message_link)
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
