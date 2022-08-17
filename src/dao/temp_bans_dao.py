"""The classes and functions handling data access objects for the temporary bans table"""
from datetime import datetime
from db_connection.db_connector import DBConnection

class TempBansDAO:
    """A data access object for temporary bans
    Attributes:
        db_connection: An object that handles database connections
        time_convert: An object that handles conversion between datetime and string"""

    def __init__(self, db_address):
        """Create a new data access object for temporary bans
        Args:
            db_address: The address for the database file where the reminders table resides"""

        self.db_connection = DBConnection(db_address)

    def get_guild_temp_bans(self, guild_id: int):
        """Get all temporary bans of a given guild
        Args:
            guild_id: The Discord ID of the guild whose temporary bans to get
        Returns: A list of Rows containing the found temporary bans"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM temporary_bans WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        temp_bans = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return temp_bans

    def get_temp_ban(self, user_id: int, guild_id: int):
        """Get a specific temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to get
            guild_id: The Discord ID of the guild from which to get the ban
        Returns: A Row object containing the found temporary ban"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM temporary_bans WHERE user_id=? AND guild_id=?"
        cursor.execute(sql, (user_id, guild_id))
        temp_ban = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return temp_ban

    def get_expired_temp_bans(self):
        """Get all expired temporary bans
        Returns: A list of Rows containing expired bans"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM temporary_bans WHERE unban_date<datetime()"
        cursor.execute(sql)
        temp_bans = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return temp_bans

    def create_temp_ban(self, user_id: int, guild_id: int, expiration: datetime):
        """Create a new temporary ban
        Args:
            user_id: The Discord ID of the user to temporarily ban
            guild_id: The Discord ID of the guild in which the user was banned
            expiration: The date when the temporary bans ends
        Returns: The database ID of the newly created temporary ban"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO temporary_bans (user_id, guild_id, unban_date) VALUES (?, ?, ?) " \
              "RETURNING id"
        cursor.execute(sql, (user_id, guild_id, expiration))
        temp_ban_id = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return temp_ban_id

    def edit_temp_ban(self, user_id: int, guild_id: int, expiration: datetime):
        """Edit an existing temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to edit
            guild_id: The Discord ID of the guild this ban is associated with
            expiration: The new expiration date for the unban"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE temporary_bans SET unban_date=? WHERE user_id=? AND guild_id=?"
        cursor.execute(sql, (expiration, user_id, guild_id))
        self.db_connection.commit_and_close(connection)

    def delete_temp_ban(self, user_id: int, guild_id: int):
        """Delete a temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to delete
            guild_id: The Discord ID of the guild from which to delete the ban"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans WHERE user_id=? AND guild_id=?"
        cursor.execute(sql, (user_id, guild_id))
        self.db_connection.commit_and_close(connection)

    def delete_user_temp_bans(self, user_id: int):
        """Delete all temporary bans of a single user
        Args:
            user_id: The Discord ID of the user whose temporary bans to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans WHERE user_id=?"
        cursor.execute(sql, (user_id,))
        self.db_connection.commit_and_close(connection)

    def delete_guild_temp_bans(self, guild_id: int):
        """Delete all temporary bans associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose temporary bans to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_temp_bans_table(self):
        """Delete every single temporary ban from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
