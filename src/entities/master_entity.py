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

    def get_discord_guild(self, client: discord.Client):
        """Get the Discord guild from the ID, if possible
        Args:
            client: The client to fetch the guild
        Returns: A discord.Guild object"""

        return client.get_guild(self.guild_id)

    def get_discord_user(self, client: discord.Client):
        """Get the Discord user from the ID, if possible
        Args:
            client: The client to fetch the user
        Returns: A discord.User object"""

        return client.get_user(self.user_id)

    def get_discord_channel(self, client: discord.Client):
        """Get the Discord channel from the ID, if possible
        Args:
            client: The client to fetch the channel
        Returns: A discord.abc.GuildChannel, discord.Thread or discord.abc.PrivateChannel object"""

        return client.get_channel(self.channel_id)

    def get_discord_role(self, client: discord.Client):
        """Get the Discord role from the ID, if possible
        Args:
            client: The client to fetch the role
        Returns: A discord.Role object"""

        return client.get_guild(self.guild_id).get_role(self.role_id)
