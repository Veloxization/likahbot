"""Guild role database rows converted into Python objects"""
from entities.master_entity import MasterEntity

class GuildRoleEntity(MasterEntity):
    """An object derived from the guild roles database table's rows
    Attributes:
        db_id: The database ID of the guild role
        role_id: The Discord ID of the guild role
        category_id: The database ID of the category this role belongs in
        guild_id: The Discord ID of the guild this role belongs in
        category: The name of the category this role belongs in"""

    def __init__(self, db_id: int, role_id: int, category_id: int, guild_id: int, category: str):
        """Create a new guild role entity
        Args:
            db_id: The database ID of the guild role
            role_id: The Discord ID of the guild role
            category_id: The database ID of the category this role belongs in
            guild_id: The Discord ID of the guild this role belongs in
            category: The name of the category this role belongs in"""

        self.db_id = db_id
        self.role_id = role_id
        self.category_id = category_id
        self.guild_id = guild_id
        self.category = category
