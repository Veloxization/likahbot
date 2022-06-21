"""Houses the cog the handles moderator setting commands"""

import discord
from discord.ext import commands
from services.utility_channel_service import UtilityChannelService

class ModeratorSettingCommands(commands.Cog):
    """This cog handles all moderator commands that have to do with general guild settings
    like where the bot will put logs.
    Attributes:
        bot: The bot the moderators assign the settings for
        utility_channel_service: Used to save the utility channel settings to the database"""

    def __init__(self, bot: discord.Client, db_address):
        """Activate the ModeratorSettingCommands cog
        Args:
            bot: The bot these settings are for
            db_address: The location of the database the bot uses"""

        self.bot = bot
        self._utility_channel_service = UtilityChannelService(db_address)
