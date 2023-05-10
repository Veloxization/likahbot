"""The classes and functions handling data access objects for the nicknames table.
The database table keeps track of a user's nickname history, including what nickname
they were and when they changed to that. Nicknames are guild specific and hence the
inclusion of an identifying guild ID is necessary"""
from db_connection.db_connector import DBConnection

class NicknamesDAO:
    """A data access object for nicknames
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for nicknames
        Args:
            db_address: The address for the database file where the nicknames table resides"""

        self.db_connection = DBConnection(db_address)

    async def find_nickname(self, nickname: str):
        """Find the instances of a given nickname within the database
        Args:
            nickname: The nickname to find in the database
        Returns: The database entries with that nickname if found, an empty list otherwise"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM nicknames WHERE nickname=?"
        await cursor.execute(sql, (nickname,))
        nicknames = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return nicknames

    async def find_user_nicknames(self, user_id: int, guild_id: int):
        """Find all nicknames for a given user
        Args:
            user_id: The Discord ID of the user whose previous nicknames to find
            guild_id: The ID of the Discord Guild the nickname is associated with
        Returns: The database entries for that user if found, an empty list otherwise"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM nicknames WHERE user_id=? AND guild_id=? ORDER BY time ASC"
        await cursor.execute(sql, (user_id, guild_id))
        nicknames = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return nicknames

    async def add_nickname(self, nickname: str, user_id: int, guild_id: int, nickname_limit: int = 5):
        """Add a new nickname to the database. If more than limit names exist already, the oldest
        are deleted.
        Args:
            nickname: The nickname to add
            user_id: The Discord ID of the user this nickname is associated with
            guild_id: The ID of the Discord Guild the nickname is associated with
            nickname_limit: How many nicknames for one user are allowed in the database at a time"""

        previous_nicknames = await self.find_user_nicknames(user_id, guild_id)
        if len(previous_nicknames) >= nickname_limit:
            this_nickname = previous_nicknames.pop()
            await self._delete_earlier_user_nicknames(user_id, guild_id, this_nickname["id"])

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO nicknames (user_id, nickname, guild_id, time) "\
              "VALUES (?, ?, ?, datetime())"
        await cursor.execute(sql, (user_id, nickname, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_nickname(self, nickname_id: int):
        """Delete a nickname from the database
        Args:
            nickname_id: The database ID for the nickname to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames WHERE id=?"
        await cursor.execute(sql, (nickname_id,))
        await self.db_connection.commit_and_close(connection)

    async def _delete_earlier_user_nicknames(self, user_id: int, guild_id: int, nickname_id: int):
        """Delete the specified nickname and any nicknames added before it
        Args:
            user_id: The Discord ID of the user whose nicknames to delete
            guild_id: The Discord ID of the guild from which the nicknames come from
            nickname_id: All nicknames added before this are deleted"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames WHERE id<=? AND user_id=? AND guild_id=?"
        await cursor.execute(sql, (nickname_id, user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_nicknames(self, user_id: int, guild_id: int):
        """Delete all nicknames associated with a specific user
        Args:
            user_id: The Discord ID for the user whose nickname history to delete
            guild_id: The ID of the Discord Guild the deleted nicknames are associated with"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_nicknames(self, guild_id: int):
        """Delete the entire nickname record of a given guild
        Args:
            guild_id: The Discord ID of the guild whose nickname records to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_nicknames_table(self):
        """Delete every single nickname from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
