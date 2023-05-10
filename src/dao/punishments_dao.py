"""The classes and functions handling data access objects for the punishments table.
The database table keeps track of a user's punishment history. Punishments include
things like kicks, bans, timeouts and warnings."""
from db_connection.db_connector import DBConnection

class PunishmentsDAO:
    """A data access object for punishments
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for punishments
        Args:
            db_address: The address for the database file where the punishments table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_user_punishments(self, user_id: int, guild_id: int):
        """Get a full list of all undeleted punishments a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose punishment history to search
            guild_id: The ID of the Discord Guild in which the punishments were given
        Returns: A list of Rows containing all the found punishments,
                 an empty list if none are found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE user_id=? " \
               "AND guild_id=? " \
               "AND deleted=FALSE " \
               "ORDER BY time DESC"
        await cursor.execute(sql, (user_id, guild_id))
        punishments = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return punishments

    async def get_all_user_punishments(self, user_id: int, guild_id: int):
        """Get a full list of all punishments a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose punishment history to search
            guild_id: The ID of the Discord Guild in which the punishments were given
        Returns: A list of Rows containing all the found punishments,
                 an empty list if none are found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE user_id=? AND guild_id=? " \
               "ORDER BY deleted ASC, time DESC"
        await cursor.execute(sql, (user_id, guild_id))
        punishments = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return punishments

    async def get_deleted_punishments(self, user_id: int, guild_id: int):
        """Get a list of punishments marked deleted a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose deleted punishments to get
            guild_id: The Discord ID of the guild in which the punishments were given
        Returns: A list of Rows containing all the found punishments"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE user_id=? AND guild_id=? AND deleted=TRUE " \
              "ORDER BY time DESC"
        await cursor.execute(sql, (user_id, guild_id))
        punishments = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return punishments

    async def get_punishment_by_id(self, punishment_id: int):
        """Get a punishment by its database ID
        Args:
            punishment_id: The database ID of the punishment to get
        Returns: A Row representing the found punishment. None if not found."""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE id=?"
        await cursor.execute(sql, (punishment_id,))
        punishment = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return punishment

    async def get_censored_punishments(self, guild_id: int):
        """Get the punishments within a given guild where the user ID has been removed
        Args:
            guild_id: The Discord Guild ID of the fuild where the punishments were issued
        Returns: A list of Rows containing all the found punishments"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE user_id=0 AND guild_id=? ORDER BY time DESC"
        await cursor.execute(sql, (guild_id,))
        punishments = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return punishments

    async def add_punishment(self, user_id: int, issuer_id: int, guild_id: int,
                       punishment_type: str = None, reason: str = None, deleted: bool = False):
        """Add a new punishment for a guild member
        Args:
            user_id: The Discord ID of the member the punishment is associated with
            issuer_id: The Discord ID of the member who issued the punishment
            guild_id: The Discord Guild ID of the guild where the punishment was issued
            punishment_type: The type of the punishment, e.g. BAN, KICK, TIMEOUT
            reason: The reason for the punishment
            deleted: Whether the punishment is deleted
        Returns: The Row for the newly created punishment"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO punishments " \
                    "(user_id, issuer_id, guild_id, type, reason, time, deleted) " \
               "VALUES " \
                    "(?, ?, ?, ?, ?, datetime(), ?) " \
               "RETURNING *"
        await cursor.execute(sql, (user_id, issuer_id, guild_id, punishment_type, reason, deleted))
        punishment = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return punishment

    async def mark_deleted(self, punishment_id: int):
        """Mark a punishment as deleted
        Args:
            punishment_id: The database ID of the punishment to mark as deleted"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET deleted=TRUE WHERE id=?"
        await cursor.execute(sql, (punishment_id,))
        await self.db_connection.commit_and_close(connection)

    async def unmark_deleted(self, punishment_id: int):
        """Mark a deleted punishment as undeleted
        Args:
            punishment_id: The database ID of the deleted punishment to mark as undeleted"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET deleted=FALSE WHERE id=?"
        await cursor.execute(sql, (punishment_id,))
        await self.db_connection.commit_and_close(connection)

    async def edit_punishment_reason(self, punishment_id: int, reason: str):
        """Edit the reason for an existing punishment
        Args:
            punishment_id: The database ID of the punishment to edit
            reason: The new reason for the punishment"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET reason=? WHERE id=?"
        await cursor.execute(sql, (reason, punishment_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_id_from_punishments(self, user_id: int):
        """Delete the mention of a given user's ID within punishments
        Args:
            user_id: The Discord ID of the user whose ID to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET user_id=0 WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_punishment(self, punishment_id: int):
        """Permanently delete a punishment
        Args:
            punishment_id: The database ID of the punishment to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM punishments WHERE id=?"
        await cursor.execute(sql, (punishment_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_punishments(self, guild_id: int):
        """Permanently delete the entire punishment record of a given guild
        Args:
            guild_id: The Discord ID of the guild whose punishment records to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM punishments WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_punishments_table(self):
        """Delete every single punishment from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM punishments"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
