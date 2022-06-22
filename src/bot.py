"""The main file that handles launching the bot.
The function assumes that, upon launch, the bot token is given as an argument.
The bot token should NEVER be hard-coded into the program. Either copy-paste
it as an argument on each launch or store it in an encrypted file and use the
decrypted value as an argument."""

import sys
import discord
from services.utility_channel_service import UtilityChannelService

DB_ADDRESS = "database/likahbotdatabase.db" # Change this to suit your database needs
debug_guilds = [383107941173166083] # Used when debugging new slash commands
bot = discord.Bot()
utility_channel_service = UtilityChannelService(DB_ADDRESS)

@bot.event
async def on_ready():
    """Runs when the bot has successfully logged in"""

    print(f"Python {sys.version}\n{sys.version_info}")
    print(f"Logged on as {bot.user}")

moderator_setting_commands = bot.create_group("guildsettings", "Adjust guild specific settings")

@moderator_setting_commands.command(name="addlogchannel", guild_ids=debug_guilds)
async def add_log_channel(
    ctx: discord.ApplicationContext,
    channel: discord.TextChannel):
    """Add a new log channel for a guild
    Args:
        ctx: The application context of the command
        channel: The channel to add as a log channel"""

    utility_channel_service.create_guild_utility_channel(channel.id, ctx.guild.id, "LOG")
    await ctx.respond(f"{channel.mention} is now a log channel. Future logs will be posted there.")

bot.run(str(sys.argv[1]))
