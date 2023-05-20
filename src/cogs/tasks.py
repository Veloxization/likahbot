"""Houses the cog for tasks, i.e. timed events"""

import discord
from discord.ext import commands, tasks
from services.temp_ban_service import TempBanService
from services.utility_channel_service import UtilityChannelService

class Tasks(commands.Cog):
    """The Tasks class houses the different tasks the bot runs in certain intervals
    Attributes:
        temp_ban_service: The service for fetching and managing temp bans
        utility_channel_service: The service for fetching and managing guild utility channels"""

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the Tasks cog
        Args:
            bot: The bot that does the tasks
            db_address: The database address where the tables for timed events reside"""

        self.bot = bot
        self.temp_ban_service = TempBanService(db_address)
        self.utility_channel_service = UtilityChannelService(db_address)
        self.unban_expired_temp_bans.start()

    @tasks.loop(minutes=1)
    async def unban_expired_temp_bans(self):
        """Checks the temp ban table for expired bans and automatically unbans applicable users"""

        temp_bans = await self.temp_ban_service.get_expired_temp_bans()
        for ban in temp_bans:
            guild = await ban.get_discord_guild(self.bot)
            user = await ban.get_discord_user(self.bot)
            try:
                await guild.unban(user, reason="Expired temp ban")
                await self.temp_ban_service.delete_temp_ban(user.id, guild.id)
            except discord.Forbidden:
                print(f"Missing permissions to unban {user} in {guild}. Skipping.")
            except discord.HTTPException:
                print(f"Can't unban {user} in {guild}. HTTPException. Skipping.")
