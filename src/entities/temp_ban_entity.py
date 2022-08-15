"""Temporary ban database rows converted into Python objects"""
from entities.master_entity import MasterEntity

class TempBanEntity(MasterEntity):
    """An object derived from the temporary_bans database table's rows
    Attributes:
        db_id: The database ID of the temporary ban
        user_id: The Discord ID of the user who was temporarily banned
        guild_id: The Discord ID of the guild where this ban was issued
        unban_date: The date when the temporary ban ends, represented as a string"""

    def __init__(self, db_id: int, user_id: int, guild_id: int, unban_date: str):
        """Create a new TempBan entity
        Args:
            db_id: The database ID of the temporary ban
            user_id: The Discord ID of the user who was temporarily banned
            guild_id: The Discord ID of the guild where this ban was issued
            unban_date: The date when the temporary ban ends, represented as a string"""

        self.db_id = db_id
        self.user_id = user_id
        self.guild_id = guild_id
        self.unban_date = unban_date
