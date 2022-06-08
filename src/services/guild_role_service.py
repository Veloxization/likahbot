"""The guild role service is used to call methods in the guild roles DAO class."""

from dao.guild_roles_dao import GuildRolesDAO
from entities.guild_role_entity import GuildRoleEntity

class GuildRoleSerivce:
    """A service for calling methods from guild roles DAO
    Attributes:
        guild_roles_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for guild roles DAO
        Args:
            db_address: The address for the database file where the guild roles table resides"""

        self.guild_roles_dao = GuildRolesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a guild role entity
        Args:
            row: The database row to convert to a guild role entity
        Returns: A guild role entity equivalent to the database row"""

        return GuildRoleEntity(row["id"], row["role_id"], row["category_id"], row["guild_id"],
                               row["category"])

    def get_all_guild_roles(self, guild_id: int):
        """Get all guild roles of a specified Guild
        Args:
            guild_id: The ID of the Discord Guild to look for roles
        Returns: A list of guild role entities"""

        rows = self.guild_roles_dao.get_all_guild_roles(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_guild_roles_of_type(self, role_category: str, guild_id: int):
        """Get all guild roles of specific type
        Args:
            role_category: The category of role to get (e.g. ADMIN, NEW, VERIFIED etc.)
            guild_id: The ID of the Discord Guild to look for roles
        Returns: A list of guild role entities"""

        rows = self.guild_roles_dao.get_guild_roles_of_type(role_category, guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_guild_roles_by_role_id(self, role_id: int):
        """Get guild roles with a specific ID
        Args:
            role_id: The ID of the role from the Discord Guild
        Returns: A list of guild role entities"""

        rows = self.guild_roles_dao.get_guild_roles_by_role_id(role_id)
        return [self._convert_to_entity(row) for row in rows]

    def add_guild_role(self, role_id: int, category_id: int):
        """Add a role under a guild role category
        Args:
            role_id: The ID of the role from the Discord Guild
            category_id: The database ID of the category this role belongs in"""

        self.guild_roles_dao.add_guild_role(role_id, category_id)

    def remove_guild_role_from_category(self, role_id: int, category_id: int):
        """Remove a guild role by the role's Discord ID
        Args:
            role_id: The Discord ID of the role to remove
            category_id: The database ID of the category to remove this role from"""

        self.guild_roles_dao.remove_guild_role_from_category(role_id, category_id)

    def delete_guild_roles(self, guild_id: int):
        """Delete all guild roles of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild roles to delete"""

        self.guild_roles_dao.delete_guild_roles(guild_id)

    def clear_guild_roles_table(self):
        """Delete every single guild role"""

        self.guild_roles_dao.clear_guild_roles_table()
