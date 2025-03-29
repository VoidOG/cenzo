import asyncio
from telethon import TelegramClient, errors
from telethon.sessions import StringSession

# Configuration
API_ID = 26075878  # Replace with your API ID
API_HASH = "7146213fe4324fcaca1bb6be7a2aef33"  # Replace with your API hash
SESSION_STRING = input("Enter your Telethon string session: ").strip()

DELAY = 3600  # Delay before the next batch

# Forum groups with specific topic IDs
FORUM_TOPICS = {
    "buffestmarket": 33,
    "stockless": 38,
    "combienforum": 11
}

async def forward_messages(client, message):
    dialogs = await client.get_dialogs()
    tasks = []

    for dialog in dialogs:
        if dialog.is_group:
            chat_username = dialog.entity.username

            async def send_to_group():
                try:
                    if chat_username in FORUM_TOPICS:
                        topic_id = FORUM_TOPICS[chat_username]
                        await client.send_message(dialog.entity, message, reply_to=topic_id)
                    else:
                        await client.forward_messages(dialog.entity.id, message)

                    print(f"✅ Message sent to {chat_username}")

                except errors.SlowModeWaitError:
                    print(f"⏩ Skipping {chat_username} due to slow mode")

                except Exception as e:
                    print(f"⚠ Error sending to {chat_username}: {e}")

            tasks.append(send_to_group())

    await asyncio.gather(*tasks)  # Send messages in parallel

async def main():
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        message_link = input("Enter the Telegram message link: ").strip()
        parts = message_link.split('/')
        chat_username = parts[-2]
        message_id = int(parts[-1])

        entity = await client.get_entity(chat_username)
        message = await client.get_messages(entity, ids=message_id)

        if not message:
            print("❌ Message not found.")
            return

        while True:
            await forward_messages(client, message)
            print(f"⏳ Waiting {DELAY} seconds before the next batch...")
            await asyncio.sleep(DELAY)

asyncio.run(main())
