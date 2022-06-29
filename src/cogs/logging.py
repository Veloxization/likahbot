"""Houses the cog that handles logging"""

import discord
from discord.ext import commands
from services.utility_channel_service import UtilityChannelService

class Logging(commands.Cog):
    """This cog handles all listeners that are used for logging events in the logging channel
    if one is defined for the guild.
    Attributes:
        bot: The bot that handles the logging
        utility_channel_service: The service used to get the logging channel"""

    def __init__(self, bot: discord.Client, db_address):
        """Activate the Logging cog
        Args:
            bot: The bot that does the logging
            db_address: The location where the bot database is located"""

        self.bot = bot
        self._utility_channel_service = UtilityChannelService(db_address)

    def _get_guild_log_channels(self, guild: discord.Guild):
        """Get the channels used for logs for a specific guild
        Args:
            guild: The Discord Guild whose log channel to get
        Returns: A list of discord.Channel objects if log channels were found"""

        channels = self._utility_channel_service.get_guild_utility_channel_by_purpose(guild.id,
                                                                                      "log")
        if not channels:
            return None
        log_channels = [channel.get_discord_channel(self.bot) for channel in channels]
        return log_channels

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Log an edited message"""

        log_channels = self._get_guild_log_channels(after.guild)
        print(len(log_channels))
        embed = discord.Embed(color=discord.Color.orange(),
                              title="Message edited",
                              description=f"Message by {after.author.mention} edited in {after.channel.mention}",
                              url=after.jump_url)
        embed.set_author(name=after.author.display_name, icon_url=after.author.avatar.url)
        embed.set_footer(text=f"ID: {after.id}")
        before_content = before.content
        after_content = after.content
        if not before_content:
            before_content = "`Could not fetch`"
        if not after_content:
            after_content = "`Could not fetch`"
        embed.add_field(name="Before", value=before_content)
        embed.add_field(name="After", value=after_content)
        for channel in log_channels:
            await channel.send(embed=embed)
