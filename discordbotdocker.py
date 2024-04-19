import discord
import re
import subprocess
import time
import asyncio
import json

# Replace 'YOUR_DISCORD_CHANNEL_ID' with the ID of the Discord channel where you want to send feedback messages
DISCORD_CHANNEL_ID = '<channel ID goes here>'

# Initialize the Discord bot with the necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Time to wait (in seconds) between posts
DEFAULT_DELAY_BETWEEN_POSTS = 300  # 5 minutes (5 minutes * 60 seconds)

# Load configuration from the storage file
def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}

# Save configuration to the storage file
def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

# Function to send feedback messages to Discord
async def send_feedback_to_discord(message):
    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    await channel.send(message)

# Function to forward a message to Nostr using noscl
async def forward_to_nostr(message_content):
    try:
        subprocess.run(['./noscl', 'publish', message_content], check=True)
    except subprocess.CalledProcessError as e:
        await send_feedback_to_discord(f'Failed to forward the message to Nostr. Error: {e}')
    except Exception as e:
        await send_feedback_to_discord(f'Error while forwarding message to Nostr: {e}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await send_feedback_to_discord('Bot is now online and ready.')

@bot.event
async def on_message(message):
    # Avoid processing messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message starts with the command prefix ("!")
    if message.content.startswith('!'):
        command = message.content.split(' ')[0].lower().lstrip('!')

        # Check for the "!delay" command
        if command == 'delay':
            try:
                # Extract the custom delay time from the command
                delay_time = int(message.content.split(' ')[1])
                if delay_time < 0:
                    await send_feedback_to_discord('Delay time cannot be negative.')
                else:
                    # Update the delay time in the configuration and save it
                    config = load_config()
                    config['delay'] = delay_time
                    save_config(config)
                    await send_feedback_to_discord(f'Delay time set to {delay_time} seconds.')
            except (IndexError, ValueError):
                await send_feedback_to_discord('Invalid delay time. Usage: !delay <seconds>')

        return  # Skip the rest of the function for command handling

    # Forward the entire message content to Nostr
    await forward_to_nostr(message.content)

    # Wait before processing the next message
    config = load_config()
    delay_time = config.get('delay', DEFAULT_DELAY_BETWEEN_POSTS)
    await asyncio.sleep(delay_time)

# Run the bot
bot.run('<ADD YOUR DICORD BOT TOKEN HERE>')
