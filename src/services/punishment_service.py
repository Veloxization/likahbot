"""The punishment service is used to call methods in the punishments DAO class."""

import hashlib
from dao.punishments_dao import PunishmentsDAO
from entities.punishment_entity import PunishmentEntity

class PunishmentService:
    """A service for calling methods from punishments DAO
    Attributes:
        punishments_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for punishments DAO
        Args:
            db_address: The address for the database file where the punishments table resides"""

        self.punishments_dao = PunishmentsDAO(db_address)

    def _convert_to_entity(self, row, user_id: int = None):
        """Convert a database row to a punishment entity
        Args:
            row: The database row to convert to a punishment entity
        Returns: A punishment entity equivalent to the database row"""

        if not row:
            return None
        return PunishmentEntity(row["id"], user_id, row["issuer_id"], row["guild_id"],
                                row["type"], row["time"], row["reason"], row["deleted"])

    async def get_user_punishments(self, user_id: int, guild_id: int):
        """Get a full list of all undeleted punishments a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose punishment history to search
            guild_id: The ID of the Discord Guild in which the punishments were given
        Returns: A list of Punishment entites containing all the found punishments"""

        h = hashlib.new("sha256")
        h.update(repr(user_id).encode())
        rows = await self.punishments_dao.get_user_punishments(h.hexdigest(), guild_id)
        return [self._convert_to_entity(row, user_id) for row in rows]

    async def get_all_user_punishments(self, user_id: int, guild_id: int):
        """Get a full list of all punishments a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose punishment history to search
            guild_id: The ID of the Discord Guild in which the punishments were given
        Returns: A list of Punishment entities containing all the found punishments"""

        h = hashlib.new("sha256")
        h.update(repr(user_id).encode())
        rows = await self.punishments_dao.get_all_user_punishments(h.hexdigest(), guild_id)
        return [self._convert_to_entity(row, user_id) for row in rows]

    async def get_punishment_by_id(self, punishment_id: int):
        """Get a punishment by its database ID
        Args:
            punishment_id: The database ID of the punishment to get
        Returns: A Punishment entity representing the found punishment. None if not found."""

        row = await self.punishments_dao.get_punishment_by_id(punishment_id)
        return self._convert_to_entity(row)

    async def get_deleted_punishments(self, user_id: int, guild_id: int):
        """Get a list of punishments marked deleted a user has within a given guild
        Args:
            user_id: The Discord ID of the user whose deleted punishments to get
            guild_id: The Discord ID of the guild in which the punishments were given
        Returns: A list of Punishment entities containing all the found punishments"""

        h = hashlib.new("sha256")
        h.update(repr(user_id).encode())
        rows = await self.punishments_dao.get_deleted_punishments(h.hexdigest(), guild_id)
        return [self._convert_to_entity(row) for row in rows]

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
        Returns: The database ID of the newly created punishment"""

        h = hashlib.new("sha256")
        h.update(repr(user_id).encode())
        row = await self.punishments_dao.add_punishment(h.hexdigest(), issuer_id, guild_id,
                                                        punishment_type, reason, deleted)
        return row["id"]

    async def mark_deleted(self, punishment_id: int):
        """Mark a punishment as deleted
        Args:
            punishment_id: The database ID of the punishment to mark as deleted"""

        await self.punishments_dao.mark_deleted(punishment_id)

    async def unmark_deleted(self, punishment_id: int):
        """Mark a deleted punishment as undeleted
        Args:
            punishment_id: The database ID of the deleted punishment to mark as undeleted"""

        await self.punishments_dao.unmark_deleted(punishment_id)

    async def edit_punishment_reason(self, punishment_id: int, reason: str):
        """Edit the reason for an existing punishment
        Args:
            punishment_id: The database ID of the punishment to edit
            reason: The new reason for the punishment"""

        await self.punishments_dao.edit_punishment_reason(punishment_id, reason)

    async def delete_punishment(self, punishment_id: int):
        """Permanently delete a punishment
        Args:
            punishment_id: The database ID of the punishment to delete"""

        await self.punishments_dao.delete_punishment(punishment_id)

    async def delete_guild_punishments(self, guild_id: int):
        """Permanently delete the entire punishment record of a given guild
        Args:
            guild_id: The Discord ID of the guild whose punishment records to delete"""

        await self.punishments_dao.delete_guild_punishments(guild_id)

    async def clear_punishments(self):
        """Delete every single punishment record"""

        await self.punishments_dao.clear_punishments_table()
