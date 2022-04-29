"""The classes and functions handling data access objects for the passphrases table"""
from db_connection.db_connector import DBConnection

class PassphrasesDAO:
    """A data access object for passphrases
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for passphrases
        Args:
            db_address: The address for the database file where the passphrases table resides"""

        self.db_connection = DBConnection(db_address)

    def get_all_guild_passphrases(self, guild_id: int):
        """Get all the passphrases a guild uses
        Args:
            guild_id: The ID of the Guild these passphrases belong to
        Returns: A list of Rows containing the passphrases of the Guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM passphrases WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        passphrases = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return passphrases

    def add_passphrase(self, guild_id: int, content: str):
        """Add a new verification passphrase to be used on a guild
        Args:
            guild_id: The ID of the Guild the passphrase is associated with
            content: The passphrase itself"""
        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO passphrases (guild_id, content) VALUES (?, ?)"
        cursor.execute(sql, (guild_id, content))
        self.db_connection.commit_and_close(connection)

    def delete_passphrase(self, passphrase_id: int):
        """Delete a passphrase
        Args:
            passphrase_id: The database ID of the passphrase to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM passphrases WHERE id=?"
        cursor.execute(sql, (passphrase_id,))
        self.db_connection.commit_and_close(connection)
