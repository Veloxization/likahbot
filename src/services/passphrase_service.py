"""The passphrase service is used to call methods in the passphrases DAO class."""

from dao.passphrases_dao import PassphrasesDAO
from entities.passphrase_entity import PassphraseEntity

class PassphraseService:
    """A service for calling methods from passphrases DAO
    Attributes:
        passphrases_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for passphrases DAO
        Args:
            db_address: The address for the database file where the passphrases table resides"""

        self.passphrases_dao = PassphrasesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a passphrase entity
        Args:
            row: The database row to convert to a passphrase entity
        Returns: A passphrase entity equivalent to the database row"""

        return PassphraseEntity(row["id"], row["guild_id"], row["content"])

    def get_all_guild_passphrases(self, guild_id: int):
        """Get all the passphrases a guild uses
        Args:
            guild_id: The ID of the Guild these passphrases belong to
        Returns: A list of Passphrase entities containing the passphrases of the Guild"""

        rows = self.passphrases_dao.get_all_guild_passphrases(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def add_passphrase(self, guild_id: int, content: str):
        """Add a new verification passphrase to be used on a guild
        Args:
            guild_id: The ID of the Guild the passphrase is associated with
            content: The passphrase itself"""

        self.passphrases_dao.add_passphrase(guild_id, content)

    def delete_passphrase(self, passphrase_id: int):
        """Delete a passphrase
        Args:
            passphrase_id: The database ID of the passphrase to delete"""

        self.passphrases_dao.delete_passphrase(passphrase_id)

    def delete_guild_passphrases(self, guild_id: int):
        """Delete all passphrases of a given guild
        Args:
            guild_id: The Discord ID of the guild whose passphrases to delete"""

        self.passphrases_dao.delete_guild_passphrases(guild_id)

    def clear_passphrases(self):
        """Delete every single passphrase"""

        self.passphrases_dao.clear_passphrases_table()
