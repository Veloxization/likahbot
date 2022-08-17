"""The temp ban service is used to call methods in the temp bans DAO class."""

from datetime import datetime
from dao.temp_bans_dao import TempBansDAO
from entities.temp_ban_entity import TempBanEntity

class TempBanService:
    """A service for calling methods from temp bans DAO
    Attributes:
        temp_bans_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for temp bans DAO
        Args:
            db_address: The address for the database file where the temporary_bans table resides"""

        self.temp_bans_dao = TempBansDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a temp ban entity
        Args:
            row: The database row to convert to a temp ban entity
        Returns: A temp ban entity equivalent to the database row"""

        if not row:
            return None
        return TempBanEntity(row["id"], row["user_id"], row["guild_id"], row["unban_date"])

    def get_guild_temp_bans(self, guild_id: int):
        """Get all temporary bans of a given guild
        Args:
            guild_id: The Discord ID of the guild whose temporary bans to get
        Returns: A list of TempBanEntities representing the found temporary bans"""

        rows = self.temp_bans_dao.get_guild_temp_bans(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_expired_temp_bans(self):
        """Get all expired temporary bans
        Returns: A list of TempBanEntities containing expired bans"""

        rows = self.temp_bans_dao.get_expired_temp_bans()
        return [self._convert_to_entity(row) for row in rows]

    def get_temp_ban(self, user_id: int, guild_id: int):
        """Get a specific temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to get
            guild_id: The Discord ID of the guild from which to get the ban
        Returns: A temp ban entity representing the found temporary ban, None if not found"""

        row = self.temp_bans_dao.get_temp_ban(user_id, guild_id)
        return self._convert_to_entity(row)

    def create_temp_ban(self, user_id: int, guild_id: int, expiration: datetime):
        """Create a new temporary ban
        Args:
            user_id: The Discord ID of the user to temporarily ban
            guild_id: The Discord ID of the guild in which the user was banned
            expiration: The date when the temporary bans ends
        Returns: The database ID of the newly created temporary ban"""

        temp_ban_id = self.temp_bans_dao.create_temp_ban(user_id, guild_id, expiration)
        return temp_ban_id

    def edit_temp_ban(self, user_id: int, guild_id: int, expiration: datetime):
        """Edit an existing temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to edit
            guild_id: The Discord ID of the guild this ban is associated with
            expiration: The new expiration date for the unban"""

        self.temp_bans_dao.edit_temp_ban(user_id, guild_id, expiration)

    def delete_temp_ban(self, user_id: int, guild_id: int):
        """Delete a temporary ban
        Args:
            user_id: The Discord ID of the user whose temporary ban to delete
            guild_id: The Discord ID of the guild from which to delete the ban"""

        self.temp_bans_dao.delete_temp_ban(user_id, guild_id)

    def delete_user_temp_bans(self, user_id: int):
        """Delete all temporary bans of a single user
        Args:
            user_id: The Discord ID of the user whose temporary bans to delete"""

        self.temp_bans_dao.delete_user_temp_bans(user_id)

    def delete_guild_temp_bans(self, guild_id: int):
        """Delete all temporary bans associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose temporary bans to delete"""

        self.temp_bans_dao.delete_guild_temp_bans(guild_id)

    def clear_temp_bans(self):
        """Delete every single temporary ban"""

        self.temp_bans_dao.clear_temp_bans_table()
