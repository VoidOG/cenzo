import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import InputPeerChannel, InputThread

# Configuration
API_ID = 26075878  # Replace with your API ID
API_HASH = "7146213fe4324fcaca1bb6be7a2aef33"  # Replace with your API hash
SESSION_STRING = input("Enter your Telethon string session: ").strip()

DELAY = 3600  # Delay in seconds between forwards

# Forum groups with specific topic IDs
FORUM_TOPICS = {
    "buffestmarket": 33,  # Example Topic ID
    "stockless": 38,      # Example Topic ID
    "combienforum": 11    # Example Topic ID
}

async def forward_messages(client, message):
    dialogs = await client.get_dialogs()

    tasks = []
    for dialog in dialogs:
        if dialog.is_group:
            chat_username = dialog.entity.username

            if chat_username in FORUM_TOPICS:
                # Send message to a specific topic inside a forum
                topic_id = FORUM_TOPICS[chat_username]
                thread = InputThread(dialog.entity.id, topic_id)
                task = client.forward_messages(thread, message)
            else:
                # Send message to normal group
                task = client.forward_messages(dialog.entity.id, message)
            
            tasks.append(task)

    await asyncio.gather(*tasks)  # Send to all groups at once
    print("Forwarded to all groups and topics.")

async def main():
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        message_link = input("Enter the Telegram message link: ").strip()
        parts = message_link.split('/')
        chat_username = parts[-2]
        message_id = int(parts[-1])

        entity = await client.get_entity(chat_username)
        message = await client.get_messages(entity, ids=message_id)

        if not message:
            print("Message not found.")
            return

        while True:
            await forward_messages(client, message)
            print(f"Waiting {DELAY} seconds before next batch...")
            await asyncio.sleep(DELAY)

asyncio.run(main())
