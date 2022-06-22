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

@moderator_setting_commands.command(name="addutilitychannel", guild_ids=debug_guilds)
async def add_utility_channel(
    ctx: discord.ApplicationContext,
    utility: discord.Option(str,
                            "The utility to add for a channel",
                            choices=["log", "rules", "verification"]),
    channel: discord.Option(discord.TextChannel, "The channel to apply the utility to")):
    """Assign a channel for a specified utility"""

    if utility not in ("log", "rules", "verification"):
        await ctx.respond(f"I am not sure what \"{utility}\" is.")
        return

    utility_channel_service.create_guild_utility_channel(channel.id, ctx.guild.id, utility)
    if utility == "log":
        await ctx.respond(f"{channel.mention} is now a log channel. Future logs will be posted there.")
    if utility == "rules":
        await ctx.respond(f"{channel.mention} is now a rules channel. If you've specified any rules, they will be posted and maintained there.")
    if utility == "verification":
        await ctx.respond(f"{channel.mention} is now a verification channel. New members can verify through this channel from now on.")

bot.run(str(sys.argv[1]))
