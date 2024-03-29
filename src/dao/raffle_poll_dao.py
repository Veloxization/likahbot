"""The classes and functions handling data access objects for the raffles_and_polls table.
Raffles are something users can opt into, usually to win something. Winners are randomly selected
from opted-in users.
Polls are used to gauge user opinions from multiple options."""
from datetime import datetime
from db_connection.db_connector import DBConnection
from time_handler.time import TimeStringConverter

class RafflesAndPollsDAO:
    """A data access object for raffles_and_polls
    Attributes:
        db_connection: An object that handles database connections
        time_convert: An object that handles conversion between datetime and string"""

    def __init__(self, db_address):
        """Create a new data access object for raffles_and_polls
        Args:
            db_address: The address for the database file where the raffles_and_polls table
                        resides"""

        self.db_connection = DBConnection(db_address)
        self.time_convert = TimeStringConverter()

    async def get_raffles(self):
        """Get all raffles
        Returns: A list of Rows containing the raffle information"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM raffles_and_polls WHERE type='RAFFLE' ORDER BY end_date ASC"
        await cursor.execute(sql)
        raffles = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return raffles

    async def get_polls(self):
        """Get all polls
        Returns: A list of Rows containing the poll information"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM raffles_and_polls WHERE type='POLL' ORDER BY end_date ASC"
        await cursor.execute(sql)
        raffles = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return raffles

    async def find_raffle_or_poll(self, channel_id: int, message_id: int):
        """Find a raffle or poll by channel and message IDs
        Args:
            channel_id: The ID of the channel where the raffle or poll is held
            message_id: The ID of the message that contains the raffle or poll information
        Returns: A Row object containing the found raffle, None if none are found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM raffles_and_polls WHERE channel_id=? AND message_id=?"
        await cursor.execute(sql, (channel_id, message_id))
        raffle = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return raffle

    async def add_raffle(self, organizer_id: int, channel_id: int, message_id: int, guild_id: int,
                   name: str, end_date: datetime, description: str = None):
        """Create a new raffle
        Args:
            organizer_id: The Discord ID of the organizer of this raffle
            channel_id: The ID of the channel where this raffle is posted
            message_id: The ID of the message containing the raffle information
            guild_id: The ID of the guild where the raffle is being held
            name: The title of the raffle
            end_date: The date and time this raffle ends
            description: The description for this raffle"""

        connection, cursor = await self.db_connection.connect_to_db()
        end_date = self.time_convert.datetime_to_string(end_date)
        sql = "INSERT INTO raffles_and_polls " \
              "(organizer_id, channel_id, message_id, guild_id, type, name, description, end_date) " \
              "VALUES (?, ?, ?, ?, 'RAFFLE', ?, ?, ?)"
        await cursor.execute(sql, (organizer_id, channel_id, message_id, guild_id,
                                   name, description, end_date))
        await self.db_connection.commit_and_close(connection)

    async def add_poll(self, organizer_id: int, channel_id: int, message_id: int, guild_id: int,
                 name: str, end_date: datetime, description: str = None):
        """Create a new poll
        Args:
            organizer_id: The Discord ID of the organizer of this poll
            channel_id: The ID of the channel where this poll is posted
            message_id: The ID of the message containing the poll information
            guild_id: The ID of the guild where the poll is being held
            name: The title of the poll
            end_date: The date and time this poll ends
            description: The description for this poll"""

        connection, cursor = await self.db_connection.connect_to_db()
        end_date = self.time_convert.datetime_to_string(end_date)
        sql = "INSERT INTO raffles_and_polls " \
              "(organizer_id, channel_id, message_id, guild_id, type, name, description, end_date) " \
              "VALUES (?, ?, ?, ?, 'POLL', ?, ?, ?)"
        await cursor.execute(sql, (organizer_id, channel_id, message_id, guild_id,
                                   name, description, end_date))
        await self.db_connection.commit_and_close(connection)

    async def remove_raffle_or_poll(self, raffle_poll_id: int):
        """Remove the selected raffle or poll
        Args:
            raffle_poll_id: The database ID of the raffle or poll to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM raffles_and_polls WHERE id=?"
        await cursor.execute(sql, (raffle_poll_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_raffles_and_polls(self, guild_id: int):
        """Delete all raffles and polls of a given guild
        Args:
            guild_id: The Discord ID of the guild whose raffles and polls to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM raffles_and_polls WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)
