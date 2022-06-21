"""Guild role category database rows converted into Python objects"""
from entities.master_entity import MasterEntity

class GuildRoleCategoryEntity(MasterEntity):
    """An object derived from the guild role categories database table's rows
    Attributes:
        db_id: The database ID of the guild role category
        guild_id: The Discord ID of the guild this category is tied to
        category: The category name, e.g. BIRTHDAY, MODERATOR, ADMIN etc."""

    def __init__(self, db_id: int, guild_id: int, category: str):
        self.db_id = db_id
        self.guild_id = guild_id
        self.category = category
