"""The classes and functions handling data access objects for the temporary bans table.
Temporary bans function like regular bans but the bot will unban temp-banned users automatically
once the specified ban time has expired."""
from datetime import datetime
from db_connection.db_connector import DBConnection

class TempBansDAO:
    """A data access object for temporary bans
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for temporary bans
        Args:
            db_address: The address for the database file where the temp bans table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_guild_temp_bans(self, guild_id: int):
        """Get all temporary bans of a given guild
        Args:
            guild_id: The Discord ID of the guild whose temporary bans to get
        Returns: A list of Rows containing the found temporary bans"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM temporary_bans WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        temp_bans = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return temp_bans

    async def get_temp_ban(self, user_id: int, guild_id: int):
        """Get a specific temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to get
            guild_id: The Discord ID of the guild from which to get the ban
        Returns: A Row object containing the found temporary ban"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM temporary_bans WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (user_id, guild_id))
        temp_ban = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return temp_ban

    async def get_expired_temp_bans(self):
        """Get all expired temporary bans
        Returns: A list of Rows containing expired bans"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM temporary_bans WHERE unban_date<datetime()"
        await cursor.execute(sql)
        temp_bans = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return temp_bans

    async def create_temp_ban(self, user_id: int, guild_id: int, expiration: datetime):
        """Create a new temporary ban
        Args:
            user_id: The Discord ID of the user to temporarily ban
            guild_id: The Discord ID of the guild in which the user was banned
            expiration: The date when the temporary bans ends
        Returns: A Row object containing the database ID of the newly created temporary ban"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO temporary_bans (user_id, guild_id, unban_date) VALUES (?, ?, ?) " \
              "RETURNING id"
        await cursor.execute(sql, (user_id, guild_id, expiration))
        temp_ban_id = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return temp_ban_id

    async def edit_temp_ban(self, user_id: int, guild_id: int, expiration: datetime):
        """Edit an existing temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to edit
            guild_id: The Discord ID of the guild this ban is associated with
            expiration: The new expiration date for the unban"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE temporary_bans SET unban_date=? WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (expiration, user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_temp_ban(self, user_id: int, guild_id: int):
        """Delete a temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to delete
            guild_id: The Discord ID of the guild from which to delete the ban"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans WHERE user_id=? AND guild_id=?"
        await cursor.execute(sql, (user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_temp_bans(self, user_id: int):
        """Delete all temporary bans of a single user
        Args:
            user_id: The Discord ID of the user whose temporary bans to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_temp_bans(self, guild_id: int):
        """Delete all temporary bans associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose temporary bans to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_temp_bans_table(self):
        """Delete every single temporary ban from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM temporary_bans"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
