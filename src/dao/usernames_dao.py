"""The classes and functions handling data access objects for the usernames table
The database table keeps track of a user's username history, including what username
they were and when they changed to that."""
from db_connection.db_connector import DBConnection

class UsernamesDAO:
    """A data access object for usernames
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for usernames
        Args:
            db_address: The address for the database file where the usernames table resides"""

        self.db_connection = DBConnection(db_address)

    async def find_username(self, username: str):
        """Find the instances of a given username within the database
        Args:
            username: The username to find in the database
        Returns: The database entries with that username if found, an empty list otherwise"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM usernames WHERE username=?"
        await cursor.execute(sql, (username,))
        usernames = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return usernames

    async def find_user_usernames(self, user_id: int):
        """Find all usernames for a given user
        Args:
            user_id: The Discord ID of the user whose previous usernames to find
        Returns: The database entries for that user if found, an empty list otherwise"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM usernames WHERE user_id=? ORDER BY time ASC"
        await cursor.execute(sql, (user_id,))
        usernames = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return usernames

    async def add_username(self, username: str, user_id: int, username_limit: int = 5):
        """Add a new username to the database. If more than limit names exist already,
           the oldest are deleted.
        Args:
            username: The username to add
            user_id: The Discord ID of the user this username is associated with
            username_limit: How many usernames for one user are allowed in the database at a time"""

        previous_usernames = await self.find_user_usernames(user_id)
        if len(previous_usernames) >= username_limit:
            this_username = previous_usernames.pop()
            await self._delete_earlier_usernames(user_id, this_username["id"])

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO usernames (user_id, username, time) VALUES (?, ?, datetime())"
        await cursor.execute(sql, (user_id, username))
        await self.db_connection.commit_and_close(connection)

    async def delete_username(self, username_id: int):
        """Delete a username from the database
        Args:
            username_id: The database ID for the username to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM usernames WHERE id=?"
        await cursor.execute(sql, (username_id,))
        await self.db_connection.commit_and_close(connection)

    async def _delete_earlier_usernames(self, user_id: int, username_id: int):
        """Delete the specified username and any usernames added before it
        Args:
            user_id: The Discord ID of the user whose usernames to delete
            username_id: All nicknames added before this are deleted"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM usernames WHERE id<=? AND user_id=?"
        await cursor.execute(sql, (username_id, user_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_usernames(self, user_id: int):
        """Delete all usernames associated with a specific user
        Args:
            user_id: The Discord ID for the user whose username history to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM usernames WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_usernames_table(self):
        """Delete every single username from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM usernames"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
