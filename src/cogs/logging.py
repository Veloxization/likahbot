"""Houses the cog that handles logging"""

import discord
from discord.ext import commands
from services.utility_channel_service import UtilityChannelService

class Logging(commands.Cog):
    """This cog handles all listeners that are used for logging events in the logging channel
    if one is defined for the guild.
    Attributes:
        bot: The bot that handles the logging
        utility_channel_service: The service used to get the logging channel
        log_channels: A dictionary containing cached log channels for guilds to avoid continuous
                      database calls. {Guild object: [Channel objects]}"""

    def __init__(self, bot: discord.Client, db_address):
        """Activate the Logging cog
        Args:
            bot: The bot that does the logging
            db_address: The location where the bot database is located"""

        self.bot = bot
        self._utility_channel_service = UtilityChannelService(db_address)
        self._log_channels = {}

    def _get_guild_log_channels(self, guild: discord.Guild):
        """Get the channels used for logs for a specific guild
        Args:
            guild: The Discord Guild whose log channel to get
        Returns: A list of discord.Channel objects if log channels were found"""

        if guild in self._log_channels:
            return self._log_channels[guild]
        channels = self._utility_channel_service.get_guild_utility_channel_by_purpose(guild.id,
                                                                                      "LOG")
        self._log_channels[guild] = channels
        return channels

    def clear_cache(self):
        """Completely clear the log channel cache"""

        self._log_channels = {}

    def delete_guild_from_cache(self, guild: discord.Guild):
        """Delete a guild's log channels from cache
        Args:
            guild: The Discord Guild whose log channels to delete from cache"""

        if guild in self._log_channels:
            self._log_channels.pop(guild)
