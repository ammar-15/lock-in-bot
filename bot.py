import discord
import os
import random
from dotenv import load_dotenv
from message import messages  # Import messages from message.py
import asyncio
from datetime import datetime, timedelta

# Load the environment variables
load_dotenv()

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load the bot token from an environment variable
TOKEN = os.getenv("TOKEN")

# Folder containing images
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")  # Ensure correct path

# Channel ID where the bot will send the message (replace with your channel ID)
CHANNEL_ID = int(os.getenv("CHANNEL_ID_1"))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(send_daily_message())  # Start the background task

async def send_daily_message():
    while True:
        now = datetime.now()
        
        # Calculate the time for 9 AM
        target_time = datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=9, minutes=1)
        if now > target_time:
            target_time += timedelta(days=1)  # Schedule for the next day if 9 AM has passed
        
        time_to_wait = (target_time - now).total_seconds()

        print(f"Waiting for {time_to_wait} seconds until 9 AM.")
        await asyncio.sleep(time_to_wait)  # Wait until 9 AM

        # Your code to send the image and message


        try:
            channel = client.get_channel(CHANNEL_ID)
            if not channel:
                print("Channel not found. Check the CHANNEL_ID.")
                return

            # Select a random image
            images = os.listdir(IMAGE_FOLDER)
            if images:
                random_image = random.choice(images)
                file_path = os.path.join(IMAGE_FOLDER, random_image)

                # Select a random message
                random_message = random.choice(messages)

                print(f"Sending image: {file_path} with message: {random_message}")  # Debugging

                # Send the image with the random message
                await channel.send(content=random_message, file=discord.File(file_path))
            else:
                print("No images available.")
        except Exception as e:
            print(f"Error in send_daily_message: {e}")


# Run the bot
client.run(TOKEN)
