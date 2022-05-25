"""The classes and functions handling data access objects for the unverified kick rules table"""
from db_connection.db_connector import DBConnection

class UnverifiedKickRulesDAO:
    """A data access object for unverified kick rules
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for unverified kick rules
        Args:
            db_address: The address for the database file where the unverified kick rules
                        table resides"""

        self.db_connection = DBConnection(db_address)

    def get_guild_unverified_kick_rules(self, guild_id: int):
        """Get the rules for kicking unverified members from specified guild
        Args:
            guild_id: The Discord ID of the guild whose kick rules to get
        Returns: A Row object containing the kick timing of the specified guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT timedelta FROM unverified_kick_rules WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        kick_rule = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return kick_rule

    def add_guild_unverified_kick_rules(self, guild_id: int, kick_timing: int):
        """Create a new unverified kick rule for a guild
        Args:
            guild_id: The Discord ID of the guild which will be getting this kick rule
            kick_timing: The time, in seconds, it takes before an unverified member is kicked,
                         counted from the time of joining the guild."""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO unverified_kick_rules (guild_id, timedelta) VALUES (?, ?)"
        cursor.execute(sql, (guild_id, kick_timing))
        self.db_connection.commit_and_close(connection)

    def edit_guild_unverified_kick_rules(self, guild_id: int, kick_timing: int):
        """Edit the timing for a guild's unverified kick timing
        Args:
            guild_id: The Discord ID of the guild whose kick rules to edit
            kick_timing: The new time, in seconds, it takes before and unverified member is
                         kicked"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE unverified_kick_rules SET timedelta=? WHERE guild_id=?"
        cursor.execute(sql, (kick_timing, guild_id))
        self.db_connection.commit_and_close(connection)

    def remove_guild_unverified_kick_rules(self, guild_id: int):
        """Remove the kick rules of a specific guild
        Args:
            guild_id: The Discord ID of the guild whose kick rules to remove"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_kick_rules WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_unverified_kick_rules_table(self):
        """Delete every single unverified kick rule from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_kick_rules"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
