"""The classes and functions handling data access objects for the utility_channels table.
The database table keeps track of channels used for varying purposes within a guild.
A specified channel could be a rule channel, or maybe a channel where the bot posts logs
or welcoming messages."""
from db_connection.db_connector import DBConnection

class UtilityChannelsDAO:
    """A data access object for utility channels
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for utility channels
        Args:
            db_address: The address for the database file where the utility channels table
            resides"""

        self.db_connection = DBConnection(db_address)

    async def get_guild_utility_channel_by_purpose(self, guild_id: int, channel_purpose: str):
        """Get a list of specific utility channels a guild uses
        Args:
            guild_id: The Discord ID of the guild whose channels to get
            channel_purpose: The purpose of the utility channels to get (e.g. RULES)
        Returns: A list of Rows with all the channels found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM utility_channels WHERE guild_id=? AND channel_purpose=? " \
              "ORDER BY channel_id ASC"
        await cursor.execute(sql, (guild_id, channel_purpose))
        channels = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return channels

    async def get_all_guild_utility_channels(self, guild_id: int):
        """Get a list of all utility channels a specific guild uses
        Args:
            guild_id: The Discord ID of the guild whose channels to get
        Returns: A list of Rows containing all the utility channels"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM utility_channels WHERE guild_id=? " \
              "ORDER BY channel_id ASC, channel_purpose ASC"
        await cursor.execute(sql, (guild_id,))
        channels = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return channels

    async def get_guild_utility_channel_by_id(self, guild_id: int, channel_id: int):
        """Get a specific channel if a guild uses it as a utility channel
        Args:
            guild_id: The Discord ID of the guild whose channel to get
            channel_id: The Discord ID of the channel to get
        Returns: A list of Rows containing all the different utilities for this channel"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM utility_channels WHERE guild_id=? AND channel_id=? " \
              "ORDER BY channel_purpose ASC"
        await cursor.execute(sql, (guild_id, channel_id))
        channel = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return channel

    async def create_guild_utility_channel(self, channel_id: int, guild_id: int, channel_purpose: str):
        """Create a new guild utility channel
        Args:
            channel_id: The Discord ID of the channel to be made into a utility channel
            guild_id: The Discord ID of the guild in which the channel resides
            channel_purpose: The purpose of the utility channel (e.g. LOGS)"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO utility_channels (channel_id, guild_id, channel_purpose)" \
              "VALUES (?, ?, ?)"
        await cursor.execute(sql, (channel_id, guild_id, channel_purpose))
        await self.db_connection.commit_and_close(connection)

    async def delete_utility_channel(self, channel_id: int, guild_id: int):
        """Stop using a specific channel as a utility channel
        Args:
            channel_id: The Discord ID of the channel to no longer be used as a utility channel
            guild_id: The Discord ID of the guild where the channel resides"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM utility_channels WHERE channel_id=? AND guild_id=?"
        await cursor.execute(sql, (channel_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_utility_from_channel(self, channel_id: int, guild_id: int, channel_purpose: str):
        """Stop using a specific channel as a specific utility channel
        Args:
            channel_id: The Discord ID of the channel to remove a utility from
            guild_id: The Discord ID of the guild where the channel resides
            channel_purpose: The purpose to remove from the channel"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM utility_channels WHERE channel_id=? AND guild_id=? AND channel_purpose=?"
        await cursor.execute(sql, (channel_id, guild_id, channel_purpose))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_utility_channels(self, guild_id: int):
        """Delete all utility channels used by a guild
        Args:
            guild_id: The Discord ID of the guild whose utility channels to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM utility_channels WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_utility_channels_table(self):
        """Delete every single utility channel from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM utility_channels"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
