"""The main file that handles launching the bot.
The function assumes that, upon launch, the bot token is given as an argument.
The bot token should NEVER be hard-coded into the program. Either copy-paste
it as an argument on each launch or store it in an encrypted file and use the
decrypted value as an argument."""

import sys
import discord
from cogs.guildsettings import GuildSettings

DB_ADDRESS = "database/likahbotdatabase.db" # Change this to suit your database needs
bot = discord.Bot()

@bot.event
async def on_ready():
    """Runs when the bot has successfully logged in"""

    print(f"Python {sys.version}\n{sys.version_info}")
    print(f"Logged on as {bot.user}")
    bot.add_cog(GuildSettings(bot, DB_ADDRESS))
    await bot.sync_commands()

bot.run(str(sys.argv[1]))
