"""The guild role category service is used to call methods in the guild role categories DAO
class."""

from dao.guild_role_categories_dao import GuildRoleCategoriesDAO
from entities.guild_role_category_entity import GuildRoleCategoryEntity

class GuildRoleCategoryService:
    """A service for calling methods from guild role categories DAO
    Attributes:
        guild_role_categories_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for guild role categories DAO
        Args:
            db_address: The address for the database file where the guild role categories table
                        resides"""

        self.guild_role_categories_dao = GuildRoleCategoriesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a guild role category entity
        Args:
            row: The database row to convert to a guild row category entity
        Returns: A guild role category entity equivalent to the database row"""

        if not row:
            return None
        return GuildRoleCategoryEntity(row["id"], row["guild_id"], row["category"])

    async def get_all_guild_role_categories(self, guild_id: int):
        """Get all guild role categories of a given guild
        Args:
            guild_id: The Discord ID of the guild whose role categories to get
        Returns: A list of guild role category entities"""

        rows = await self.guild_role_categories_dao.get_all_guild_role_categories(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    async def add_guild_role_category(self, guild_id: int, category: str):
        """Add a new guild role category for a given guild
        Args:
            guild_id: The Discord ID of the guild that gets the new category
            category: The type of category, e.g. MODERATOR or ADMIN"""

        await self.guild_role_categories_dao.add_guild_role_category(guild_id, category)

    async def remove_guild_role_category(self, category_id: int):
        """Remove a guild role category by its database ID
        Args:
            category_id: The database ID of the category to remove"""

        await self.guild_role_categories_dao.remove_guild_role_category(category_id)

    async def remove_all_guild_role_categories(self, guild_id: int):
        """Remove all guild role categories of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild role categories to remove"""

        await self.guild_role_categories_dao.remove_all_guild_role_categories(guild_id)

    async def clear_guild_role_categories(self):
        """Delete every single guild role category"""

        await self.guild_role_categories_dao.clear_guild_role_categories_table()
