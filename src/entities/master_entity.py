"""Houses the MasterEntity class"""
import discord

class MasterEntity():
    """All entities are subclasses of this class. This master class includes the calls to the
    Pycord library itself."""
    def __init__(self):
        self.user_id = None
        self.guild_id = None
        self.channel_id = None
        self.role_id = None

    async def get_discord_guild(self, client: discord.Client):
        """Get the Discord guild from the ID, if possible
        Args:
            client: The client to fetch the guild
        Returns: A discord.Guild object or str if not found"""

        guild = client.get_guild(self.guild_id)
        if not guild:
            try:
                guild = await client.fetch_guild(self.guild_id)
            except discord.NotFound:
                guild = f"Unknown guild with ID {self.guild_id}"
        return guild

    async def get_discord_user(self, client: discord.Client):
        """Get the Discord user from the ID, if possible
        Args:
            client: The client to fetch the user
        Returns: A discord.User object or str if not found"""

        user = client.get_user(self.user_id)
        if not user:
            try:
                user = await client.fetch_user(self.user_id)
            except discord.NotFound:
                user = f"Unknown user with ID {self.user_id}"
        return user

    async def get_discord_channel(self, client: discord.Client):
        """Get the Discord channel from the ID, if possible
        Args:
            client: The client to fetch the channel
        Returns: A discord.abc.GuildChannel, discord.Thread or discord.abc.PrivateChannel object,
                 or str if not found"""

        channel = client.get_channel(self.channel_id)
        if not channel:
            try:
                channel = await client.fetch_channel(self.channel_id)
            except discord.NotFound:
                channel = f"Unknown channel with ID {self.channel_id}"
        return channel

    async def get_discord_role(self, client: discord.Client):
        """Get the Discord role from the ID, if possible
        Args:
            client: The client to fetch the role
        Returns: A discord.Role object or str if not found"""

        guild = self.get_discord_guild(client)
        if not isinstance(guild, discord.Guild) or not guild:
            return f"Unknown role with ID {self.role_id}"
        role = guild.get_role(self.role_id)
        if not role:
            role = f"Unknown role with ID {self.role_id}"
        return role
