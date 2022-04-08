"""The classes and functions handling data access objects for the usernames table"""
from datetime import datetime
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

    def find_username(self, username: str):
        """Find the instances of a given username within the database
        Args:
            username: The username to find in the database
        Returns: The database entries with that username if found, an empty list otherwise"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM usernames WHERE username=?"
        cursor.execute(sql, (username,))
        usernames = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return usernames

    def find_user_usernames(self, user_id: int):
        """Find all usernames for a given user
        Args:
            user_id: The Discord ID of the user whose previous usernames to find
        Returns: The database entries for that user if found, an empty list otherwise"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM usernames WHERE user_id=? ORDER BY time ASC"
        cursor.execute(sql, (user_id,))
        usernames = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return usernames

    def add_username(self, username: str, user_id: int, time: datetime, username_limit: int = 5):
        """Add a new username to the database. If five names exist already, the oldest is deleted.
        Args:
            username: The username to add
            user_id: The Discord ID of the user this username is associated with
            time: The current date
            username_limit: How many usernames for one user are allowed in the database at a time"""

        previous_usernames = self.find_user_usernames(user_id)
        while len(previous_usernames) >= username_limit:
            username = previous_usernames.pop(0)
            self.delete_username(username["id"])

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO usernames (user_id, username, time) VALUES (?, ?, ?)"
        cursor.execute(sql, (user_id, username, time))
        self.db_connection.commit_and_close(connection)

    def delete_username(self, username_id: int):
        """Delete a username from the database
        Args:
            username_id: The database ID for the username to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM usernames WHERE id=?"
        cursor.execute(sql, (username_id,))
        self.db_connection.commit_and_close(connection)

    def delete_user_usernames(self, user_id: int):
        """Delete all usernames associated with a specific user
        Args:
            user_id: The Discord ID for the user whose username history to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM usernames WHERE user_id=?"
        cursor.execute(sql, (user_id,))
        self.db_connection.commit_and_close(connection)
