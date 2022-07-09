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

    def get_user_punishments(self, user_id: int, guild_id: int):
        """Get a full list of all undeleted punishments a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose punishment history to search
            guild_id: The ID of the Discord Guild in which the punishments were given
        Returns: A list of Rows containing all the found punishments,
                 an empty list if none are found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE user_id=? " \
               "AND guild_id=? " \
               "AND deleted=FALSE " \
               "ORDER BY time ASC"
        cursor.execute(sql, (user_id, guild_id))
        punishments = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return punishments

    def get_all_user_punishments(self, user_id: int, guild_id):
        """Get a full list of all punishments a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose punishment history to search
            guild_id: The ID of the Discord Guild in which the punishments were given
        Returns: A list of Rows containing all the found punishments,
                 an empty list if none are found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM punishments WHERE user_id=? AND guild_id=? " \
               "ORDER BY time ASC, deleted DESC"
        cursor.execute(sql, (user_id, guild_id))
        punishments = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return punishments

    def add_punishment(self, user_id: int, issuer_id: int, guild_id: int,
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

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO punishments " \
                    "(user_id, issuer_id, guild_id, type, reason, time, deleted) " \
               "VALUES " \
                    "(?, ?, ?, ?, ?, datetime(), ?) " \
               "RETURNING *"
        cursor.execute(sql, (user_id, issuer_id, guild_id, punishment_type, reason, deleted))
        punishment = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return punishment

    def mark_deleted(self, punishment_id: int):
        """Mark a punishment as deleted
        Args:
            punishment_id: The database ID of the punishment to mark as deleted"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET deleted=TRUE WHERE id=?"
        cursor.execute(sql, (punishment_id,))
        self.db_connection.commit_and_close(connection)

    def unmark_deleted(self, punishment_id: int):
        """Mark a deleted punishment as undeleted
        Args:
            punishment_id: The database ID of the deleted punishment to mark as undeleted"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET deleted=FALSE WHERE id=?"
        cursor.execute(sql, (punishment_id,))
        self.db_connection.commit_and_close(connection)

    def edit_punishment_reason(self, punishment_id: int, reason: str):
        """Edit the reason for an existing punishment
        Args:
            punishment_id: The database ID of the punishment to edit
            reason: The new reason for the punishment"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE punishments SET reason=? WHERE id=?"
        cursor.execute(sql, (reason, punishment_id))
        self.db_connection.commit_and_close(connection)

    def delete_punishment(self, punishment_id: int):
        """Permanently delete a punishment
        Args:
            punishment_id: The database ID of the punishment to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM punishments WHERE id=?"
        cursor.execute(sql, (punishment_id,))
        self.db_connection.commit_and_close(connection)

    def delete_guild_punishments(self, guild_id: int):
        """Permanently delete the entire punishment record of a given guild
        Args:
            guild_id: The Discord ID of the guild whose punishment records to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM punishments WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_punishments_table(self):
        """Delete every single punishment from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM punishments"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
