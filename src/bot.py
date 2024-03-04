"""The main file that handles launching the bot.
The function assumes that, upon launch, the bot token is given as an argument.
The bot token should NEVER be hard-coded into the program. Either copy-paste
it as an argument on each launch or store it in an encrypted file and use the
decrypted value as an argument."""

import sys
import discord
from config.constants import DB_ADDRESS
from cogs.guildsettings import GuildSettings
from cogs.logging import Logging
from cogs.modcommands import ModCommands
from cogs.tasks import Tasks
from services.guild_setting_service import GuildSettingService

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    """Runs when the bot has successfully logged in"""

    print(f"Python {sys.version}\n{sys.version_info}")
    print(f"Logged on as {bot.user}")
    bot.add_cog(GuildSettings(bot, DB_ADDRESS))
    invites = {}
    guild_setting_service = GuildSettingService(DB_ADDRESS)
    for guild in bot.guilds:
        invites[guild] = await guild.invites()
        await guild_setting_service.initialize_guild_settings(guild.id)
    bot.add_cog(Logging(bot, DB_ADDRESS, invites))
    bot.add_cog(ModCommands(bot, DB_ADDRESS))
    bot.add_cog(Tasks(bot, DB_ADDRESS))
    await bot.sync_commands()

bot.run(str(sys.argv[1]))
