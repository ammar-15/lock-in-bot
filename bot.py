import discord
import os
import random
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load the bot token from an environment variable or hardcode for now
TOKEN = os.getenv("TOKEN")

# Folder containing images
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")  # Ensure correct path

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f"Message: {message.content}")
    if message.author == client.user:
        return

    # Command to send a random image
    if message.content.startswith('!sendimage'):
        try:
            images = os.listdir(IMAGE_FOLDER)
            if images:
                random_image = random.choice(images)
                file_path = os.path.join(IMAGE_FOLDER, random_image)
                print(f"Sending image: {file_path}")  # Debugging
                await message.channel.send(file=discord.File(file_path))
            else:
                await message.channel.send("No images available.")
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("An error occurred while sending the image.")

# Run the bot
client.run(TOKEN)
