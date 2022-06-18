"""The nickname service is used to call methods in the nicknames DAO class."""

from dao.nicknames_dao import NicknamesDAO
from entities.nickname_entity import NicknameEntity

class NicknameService:
    """A service for calling methods from nicknames DAO
    Attributes:
        nicknames_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for nicknames DAO
        Args:
            db_address: The address for the database file where the nicknames table resides"""

        self.nicknames_dao = NicknamesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a nickname entity
        Args:
            row: The database row to convert to a nickname entity
        Returns: A nickname entity equivalent to the database row"""

        if not row:
            return None
        return NicknameEntity(row["id"], row["user_id"], row["nickname"], row["guild_id"],
                              row["time"])

    def find_nickname(self, nickname: str):
        """Find the instances of a given nickname
        Args:
            nickname: The nickname to find
        Returns: A list of Nickname entities"""

        rows = self.nicknames_dao.find_nickname(nickname)
        return [self._convert_to_entity(row) for row in rows]

    def find_user_nicknames(self, user_id: int, guild_id: int):
        """Find all nicknames for a given user
        Args:
            user_id: The Discord ID of the user whose previous nicknames to find
            guild_id: The ID of the Discord Guild the nickname is associated with
        Returns: A list of Nickname entities"""

        rows = self.nicknames_dao.find_user_nicknames(user_id, guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def add_nickname(self, nickname: str, user_id: int, guild_id: int, nickname_limit: int = 5):
        """Add a new nickname. If more than limit names exist already, the oldest are deleted.
        Args:
            nickname: The nickname to add
            user_id: The Discord ID of the user this nickname is associated with
            guild_id: The ID of the Discord Guild the nickname is associated with
            nickname_limit: How many nicknames for one user are allowed to be saved at a time"""

        self.nicknames_dao.add_nickname(nickname, user_id, guild_id, nickname_limit)

    def delete_nickname(self, nickname_id: int):
        """Delete a nickname record
        Args:
            nickname_id: The database ID for the nickname to delete"""

        self.nicknames_dao.delete_nickname(nickname_id)

    def delete_user_nicknames(self, user_id: int, guild_id: int):
        """Delete all nickname records associated with a specific user
        Args:
            user_id: The Discord ID for the user whose nickname records to delete
            guild_id: The ID of the Discord Guild the deleted nicknames are associated with"""

        self.nicknames_dao.delete_user_nicknames(user_id, guild_id)

    def delete_guild_nicknames(self, guild_id: int):
        """Delete the entire nickname record of a given guild
        Args:
            guild_id: The Discord ID of the guild whose nickname records to delete"""

        self.nicknames_dao.delete_guild_nicknames(guild_id)

    def clear_nicknames(self):
        """Delete every single nickname record"""

        self.nicknames_dao.clear_nicknames_table()
