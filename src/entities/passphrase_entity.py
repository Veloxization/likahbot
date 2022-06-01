"""Passphrase database rows converted into Python objects"""

from time_handler.time import TimeStringConverter

class PassphraseEntity():
    """An object derived from the passphrases database table's rows
    Attributes:
        db_id: The database ID of the passphrase
        guild_id: The Discord ID of the guild this passphrase is tied to
        content: The passphrase string itself"""

    def __init__(self, db_id: int, guild_id: int, content: str):
        """Create a new Nickname entity
        Args:
            db_id: The database ID of the passphrase
            guild_id: The Discord ID of the guild this passphrase is tied to
            content: The passphrase string itself"""

        self.db_id = db_id
        self.guild_id = guild_id
        self.content = content
