"""Houses the cog for tasks, i.e. timed events"""

import discord
from discord.ext import commands, tasks

class Tasks(commands.Cog):
    """The Tasks class houses the different tasks the bot runs in certain intervals"""

    def __init__(self, bot: discord.Bot, db_address):
        """Activate the Tasks cog
        Args:
            bot: The bot that does the tasks
            db_address: The database address where the tables for timed events reside"""

        self.bot = bot
