"""Houses the temporary channel creator helper class"""

import discord
from errors.likah_bot_exceptions import NotDefined

class TempChannelCreator:
    """Creates temporary channels for the bot to use
    Attributes:
        bot: The bot to use
        guild: The guild for which the temporary channels are
        temp_category: The temporary category under which the channels are created"""

    def __init__(self, bot: discord.Bot, guild: discord.Guild):
        """Create a new TempChannelCreator instance
        Args:
            bot: The bot to use
            guild: The guild for which the temporary channels are"""

        self.bot = bot
        self.guild = guild
        self.temp_category = None
        self.warn_channel = None

    async def get_temp_category(self):
        """Create a temporary category for the bot to use, or get an existing one
        Returns: The created or found temporary category"""

        guild_category_names = [category.name for category in self.guild.categories]
        if "Likah Temporary Channels" not in guild_category_names:
            category = await self.guild.create_category("Likah Temporary Channels")
        else:
            for cat in self.guild.categories:
                if cat.name == "Likah Temporary Channels":
                    category = cat
                    break
        self.temp_category = category
        return self.temp_category

    async def create_warn_channel(self, member: discord.Member,
                                  warning_id: int, warning_reason: str):
        """Create a temporary warning channel for the warning
        Args:
            member: The member to warn
            warning_id: The database ID of the warning
            warning_reason: The reason for the warning
        Returns: The created warning channel"""

        if self.temp_category is None:
            raise NotDefined("Temporary Category")
        perm_dict = {
            member: discord.PermissionOverwrite(view_channel=True),
            member.guild.me: discord.PermissionOverwrite(view_channel=True),
            member.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        channel = await self.temp_category.create_text_channel(f"{member.name.replace(' ', '')}-warning-{warning_id}",
                                                               overwrites=perm_dict)
        self.warn_channel = channel
        await self.warn_channel.send(f"{member.mention}, you have been issued a warning\n" \
                                     f"Provided reason:\n`{warning_reason}`")
        return self.warn_channel
