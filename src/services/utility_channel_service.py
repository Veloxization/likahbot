"""The utility channel service is used to call methods in the utility channels DAO class."""

from dao.utility_channels_dao import UtilityChannelsDAO
from entities.utility_channel_entity import UtilityChannelEntity

class UtilityChannelService:
    """A service for calling methods from utility channels DAO
    Attributes:
        utility_channels_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for utility channels DAO
        Args:
            db_address: The address for the database file where the utility channels table
                        resides"""

        self.utility_channels_dao = UtilityChannelsDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a utility channel entity
        Args:
            row: The database row to convert to a utility channel entity
        Returns: A utility channel entity equivalent to the database row"""

        return UtilityChannelEntity(row["id"], row["channel_id"], row["guild_id"],
                                    row["channel_purpose"])

    def get_guild_utility_channel_by_purpose(self, guild_id: int, channel_purpose: str):
        """Get a list of specific utility channels a guild uses
        Args:
            guild_id: The Discord ID of the guild whose channels to get
            channel_purpose: The purpose of the utility channels to get (e.g. RULES)
        Returns: A list of utility channel entities"""

        rows = self.utility_channels_dao.get_guild_utility_channel_by_purpose(guild_id,
                                                                              channel_purpose)
        return [self._convert_to_entity(row) for row in rows]

    def get_all_guild_utility_channels(self, guild_id: int):
        """Get a list of all utility channels a specific guild uses
        Args:
            guild_id: The Discord ID of the guild whose channels to get
        Returns: A list of utility channel entities"""

        rows = self.utility_channels_dao.get_all_guild_utility_channels(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_guild_utility_channel_by_id(self, guild_id: int, channel_id: int):
        """Get a specific channel if a guild uses it as a utility channel
        Args:
            guild_id: The Discord ID of the guild whose channel to get
            channel_id: The Discord ID of the channel to get
        Returns: A utility channel entity if the channel is used as one"""

        row = self.utility_channels_dao.get_guild_utility_channel_by_id(guild_id, channel_id)
        return self._convert_to_entity(row)

    def create_guild_utility_channel(self, channel_id: int, guild_id: int, channel_purpose: str):
        """Create a new guild utility channel
        Args:
            channel_id: The Discord ID of the channel to be made into a utility channel
            guild_id: The Discord ID of the guild in which the channel resides
            channel_purpose: The purpose of the utility channel (e.g. LOGS)"""

        self.utility_channels_dao.create_guild_utility_channel(channel_id, guild_id,
                                                               channel_purpose)

    def delete_utility_channel(self, channel_id: int, guild_id: int):
        """Stop using a specific channel as a utility channel
        Args:
            channel_id: The Discord ID of the channel to no longer be used as a utility channel
            guild_id: The Discord ID of the guild where the channel resides"""

        self.utility_channels_dao.delete_utility_channel(channel_id, guild_id)

    def delete_guild_utility_channels(self, guild_id: int):
        """Delete all utility channels used by a guild
        Args:
            guild_id: The Discord ID of the guild whose utility channels to delete"""

        self.utility_channels_dao.delete_guild_utility_channels(guild_id)

    def clear_utility_channels(self):
        """Delete every single utility channel"""

        self.utility_channels_dao.clear_utility_channels_table()
