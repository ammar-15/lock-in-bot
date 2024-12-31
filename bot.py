import discord
import os
import random
from dotenv import load_dotenv
from message import messages
import asyncio
from datetime import datetime, timedelta

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.getenv("TOKEN")
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")
CHANNEL_ID = int(os.getenv("CHANNEL_ID_1"))


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    client.loop.create_task(send_daily_message())


async def send_daily_message():
    while True:
        now = datetime.now()

        target_time = datetime.combine(now.date(), datetime.min.time()) + timedelta(
            hours=9, minutes=1
        )
        if now > target_time:
            target_time += timedelta(days=1)

        time_to_wait = (target_time - now).total_seconds()

        print(f"Waiting for {time_to_wait} seconds until 9 AM.")

        await asyncio.sleep(time_to_wait)

        if now.weekday() >= 5:
            print("It's a weekend, skipping message")
            continue
        else:
            print("It's a weekday, continuing with message")

        if random.random() > 0.05:
            print("Skipping message due to 5% probability check")
            continue

        print("Passed 5% probability check, sending message")

        try:
            channel = client.get_channel(CHANNEL_ID)
            if not channel:
                print("Channel not found. Check the CHANNEL_ID.")
                return

            images = os.listdir(IMAGE_FOLDER)
            if images:
                random_image = random.choice(images)
                file_path = os.path.join(IMAGE_FOLDER, random_image)

                random_message = random.choice(messages)

                print(
                    f"Sending image: {file_path} with message: {random_message}"
                )

                await channel.send(content=random_message, file=discord.File(file_path))
            else:
                print("No images available.")
        except Exception as e:
            print(f"Error in send_daily_message: {e}")


client.run(TOKEN)
