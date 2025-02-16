import json
from telethon import TelegramClient, events, errors
import asyncio
import random
from datetime import datetime

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

API_ID = config['api_id']
API_HASH = config['api_hash']
SOURCE_CHANNEL = config['source_channel']
DESTINATION_CHANNEL = config['destination_channel']
MESSAGE_TYPES = config['message_types']
MAX_MESSAGES_PER_RUN = config['max_messages_per_run']
MIN_DELAY = config['min_delay']
MAX_DELAY = config['max_delay']


async def random_delay(min_delay=MIN_DELAY, max_delay=MAX_DELAY):
    delay = random.uniform(min_delay, max_delay)
    return delay

async def forward_messages(start_id, limit=MAX_MESSAGES_PER_RUN):
    try:
        print(f"\nStarting to forward messages from message ID: {start_id}")

        message_count = 0

        async for message in client.iter_messages(SOURCE_CHANNEL, limit=limit, offset_id=start_id, reverse=True):
            message_count += 1
            forward = False

            if "video" in MESSAGE_TYPES and message.video:
                forward = True
            elif "photo" in MESSAGE_TYPES and message.photo:
                forward = True
            elif "text" in MESSAGE_TYPES and message.text:
                forward = True
            elif "document" in MESSAGE_TYPES and message.document:
                forward = True
            elif "link" in MESSAGE_TYPES and message.message and "http" in message.message:
                forward = True

            if forward:
                try:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n[{current_time}] Forwarding message {message.id} (#{message_count})")

                    await client.send_message(DESTINATION_CHANNEL, message, silent=True)
                    print(f"✓ Successfully forwarded message ID: {message.id}")

                    delay = await random_delay()
                    await asyncio.sleep(delay)

                except errors.FloodWaitError as e:
                    wait_time = e.seconds
                    print(f"⚠️ FloodWaitError: Waiting {wait_time} seconds")
                    await asyncio.sleep(wait_time)
                    continue
                
                except errors.ChatWriteForbiddenError:
                    print("❌ Error: You don't have permission to message the channel.")
                    break

                except Exception as e:
                    print(f"❌ Error forwarding message {message.id}: {str(e)}")
                    await asyncio.sleep(60)  # Wait before retrying

    except Exception as e:
        print(f"Error during forwarding: {str(e)}")


async def main():
    try:
        print("\n=== Telegram Forwarding Script ===")
        print(f"=== Destination: {DESTINATION_CHANNEL} ===\n")

        video_link = input("Enter the message link after which to forward messages (e.g., https://t.me/YourChannel/123): ")
        start_id = int(video_link.strip().split('/')[-1])

        await client.start()

        try:
            await client.get_entity(SOURCE_CHANNEL)
        except ValueError:
            print(f"Joining source channel {SOURCE_CHANNEL}...")
            await client.join_channel(SOURCE_CHANNEL)

        await forward_messages(start_id)
        print("\n=== Forwarding complete! ===")

    except Exception as e:
        print(f"\nMain error: {str(e)}")

if __name__ == '__main__':
    with TelegramClient('forward_bot_session.session', API_ID, API_HASH) as client:
        client.loop.run_until_complete(main())