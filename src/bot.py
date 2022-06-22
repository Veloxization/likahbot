"""The main file that handles launching the bot.
The function assumes that, upon launch, the bot token is given as an argument.
The bot token should NEVER be hard-coded into the program. Either copy-paste
it as an argument on each launch or store it in an encrypted file and use the
decrypted value as an argument."""

import sys
import discord

debug_guilds = [383107941173166083] # Used when debugging new slash commands
bot = discord.Bot()

@bot.event
async def on_ready():
    """Runs when the bot has successfully logged in"""

    print(f"Python {sys.version}\n{sys.version_info}")
    print(f"Logged on as {bot.user}")
