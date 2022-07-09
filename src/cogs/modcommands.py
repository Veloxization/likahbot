"""Houses the cog that handles moderation commands"""

import discord
from discord.ext import commands
from helpers.embed_pager import EmbedPager
from services.punishment_service import PunishmentService

class ModCommands(commands.Cog):
    """This cog handles all commands that are used for moderation purposes
    Attributes:
        bot: The bot these settings apply to
        punishment_service: The service used to log punishments"""

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the mod commands cog
        Args:
            bot: The bot that runs the moderation commands
            db_address: The location of the database the bot saves data to"""

        self.bot = bot
        self.punishment_service = PunishmentService(db_address)
