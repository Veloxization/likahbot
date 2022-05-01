"""The classes and functions handling data access objects for the nicknames table"""
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

    def find_nickname(self, nickname: str):
        """Find the instances of a given nickname within the database
        Args:
            nickname: The nickname to find in the database
        Returns: The database entries with that nickname if found, an empty list otherwise"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM nicknames WHERE nickname=?"
        cursor.execute(sql, (nickname,))
        nicknames = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return nicknames

    def find_user_nicknames(self, user_id: int, guild_id: int):
        """Find all nicknames for a given user
        Args:
            user_id: The Discord ID of the user whose previous nicknames to find
            guild_id: The ID of the Discord Guild the nickname is associated with
        Returns: The database entries for that user if found, an empty list otherwise"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM nicknames WHERE user_id=? AND guild_id=? ORDER BY time ASC"
        cursor.execute(sql, (user_id, guild_id))
        nicknames = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return nicknames

    def add_nickname(self, nickname: str, user_id: int, guild_id: int, nickname_limit: int = 5):
        """Add a new nickname to the database. If five names exist already, the oldest is deleted.
        Args:
            nickname: The nickname to add
            user_id: The Discord ID of the user this nickname is associated with
            guild_id: The ID of the Discord Guild the nickname is associated with
            nickname_limit: How many nicknames for one user are allowed in the database at a time"""

        previous_nicknames = self.find_user_nicknames(user_id, guild_id)
        while len(previous_nicknames) >= nickname_limit:
            nickname = previous_nicknames.pop(0)
            self.delete_nickname(nickname["id"])

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO nicknames (user_id, nickname, guild_id, time) VALUES (?, ?, ?, datetime())"
        cursor.execute(sql, (user_id, nickname, guild_id))
        self.db_connection.commit_and_close(connection)

    def delete_nickname(self, nickname_id: int):
        """Delete a nickname from the database
        Args:
            nickname_id: The database ID for the nickname to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames WHERE id=?"
        cursor.execute(sql, (nickname_id,))
        self.db_connection.commit_and_close(connection)

    def delete_user_nicknames(self, user_id: int, guild_id: int):
        """Delete all nicknames associated with a specific user
        Args:
            user_id: The Discord ID for the user whose nickname history to delete
            guild_id: The ID of the Discord Guild the deleted nicknames are associated with"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM nicknames WHERE user_id=? AND guild_id=?"
        cursor.execute(sql, (user_id, guild_id))
        self.db_connection.commit_and_close(connection)
