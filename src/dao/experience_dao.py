"""The classes and functions handling data access objects for the experience table"""
from datetime import datetime
from db_connection.db_connector import DBConnection
from time_handler.time import TimeStringConverter, TimeDifference

class ExperienceDAO:
    """A data access object for experience
    Attributes:
        db_connection: An object that handles database connections
        time_convert: An object that handles conversion between datetime and string"""

    def __init__(self, db_address):
        """Create a new data access object for experience
        Args:
            db_address: The address for the database file where the experience table resides"""

        self.db_connection = DBConnection(db_address)
        self.time_convert = TimeStringConverter()

    async def get_guild_leaderboard(self, guild_id: int):
        """Get all experience in a Guild
        Args:
            guild_id: The ID of the Guild whose experience points to list
        Returns: A list of Rows containing the experience points of the selected Guild"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM experience WHERE guild_id=? ORDER BY amount DESC"
        await cursor.execute(sql, (guild_id,))
        experience = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return experience

    async def get_user_experience(self, user_id: int, guild_id: int):
        """Get the experience for a specific user on a specific Guild
        Args:
            user_id: The user whose experience to get
            guild_id: The ID of the Guild from which to get the experience
        Returns: A single Row with the user experience, None if no experience is found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM experience WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (user_id, guild_id))
        experience = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return experience

    async def add_user_experience(self, user_id: int, guild_id: int, amount: int, interval: int):
        """Give the user of a specific guild a specific amount of experience.
        Experience will not be awarded if time to last_experience is less than the specified
        interval.
        Args:
            user_id: The Discord ID of the user who gets the experience
            guild_id: The ID of the Guild on which the experience is awarded
            amount: The amount of experience to award
            interval: The interval, in seconds, after which the user is eligible for more
                      experience"""

        experience = await self.get_user_experience(user_id, guild_id)
        connection, cursor = await self.db_connection.connect_to_db()
        if not experience:
            sql = "INSERT INTO experience (user_id, guild_id, last_experience, amount) " \
                   "VALUES (?, ?, datetime(), ?)"
            await cursor.execute(sql, (user_id, guild_id, amount))
        else:
            last_experience = await self.time_convert.string_to_datetime(experience["last_experience"])
            time_difference = TimeDifference().time_difference(last_experience, datetime.utcnow())
            if time_difference > interval:
                sql = "UPDATE experience SET amount=amount+?, last_experience=datetime() WHERE user_id=? AND guild_id=?"
                await cursor.execute(sql, (amount, user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def reset_user_experience(self, user_id: int, guild_id: int):
        """Reset a user's experience in a Guild back to 0
        Args:
            user_id: The Discord ID of the user whose experience to reset
            guild_id: The ID of the guild in which the experience is reset"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE experience SET amount=0, last_experience=datetime() WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_experience(self, user_id: int, guild_id: int):
        """Delete the database entry for a user's experience
        Args:
            user_id: The Discord ID of the user whose experience to delete
            guild_id: The ID of the guild from which to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM experience WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_experience(self, guild_id: int):
        """Delete all experience records for a given guild
        Args:
            guild_id: The Discord ID of the guild whose experience records to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM experience WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)
