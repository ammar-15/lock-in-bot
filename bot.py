import discord
import os
import random
from dotenv import load_dotenv
from message import messages  # Import messages from message.py

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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f"Message: {message.content}")
    if message.author == client.user:
        return

    # Command to send a random image with a random message
    if message.content.startswith('!sendimage'):
        try:
            images = os.listdir(IMAGE_FOLDER)
            if images:
                # Select a random image
                random_image = random.choice(images)
                file_path = os.path.join(IMAGE_FOLDER, random_image)
                
                # Select a random message
                random_message = random.choice(messages)
                
                print(f"Sending image: {file_path} with message: {random_message}")  # Debugging
                
                # Send the image with the random message
                await message.channel.send(content=random_message, file=discord.File(file_path))
            else:
                await message.channel.send("No images available.")
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("An error occurred while sending the image.")

# Run the bot
client.run(TOKEN)
