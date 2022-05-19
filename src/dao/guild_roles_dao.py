"""The classes and functions handling data access objects for the guild_roles table"""
from db_connection.db_connector import DBConnection

class GuildRolesDAO:
    """A data access object for guild roles
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for guild roles
        Args:
            db_address: The address for the database file where the guild_roles table resides"""

        self.db_connection = DBConnection(db_address)

    def get_all_guild_roles(self, guild_id: int):
        """Get all specified roles of a specified Guild
        Args:
            guild_id: The ID of the Discord Guild to look for roles
        Returns:
            A list of Rows containing the found roles"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_roles WHERE guild_id=? ORDER BY type ASC"
        cursor.execute(sql, (guild_id,))
        roles = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return roles

    def get_guild_roles_of_type(self, role_type: str, guild_id: int):
        """Get all Guild roles of specific type
        Args:
            role_type: The type of role to get (e.g. ADMIN, NEW, VERIFIED etc.)
            guild_id: The ID of the Discord Guild to look for roles
        Returns:
            A list of Rows containing the found roles"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_roles WHERE type=? AND guild_id=?"
        cursor.execute(sql, (role_type, guild_id))
        roles = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return roles

    def get_guild_role_by_role_id(self, role_id: int):
        """Get a role of a specific ID
        Args:
            role_id: The ID of the role from the Discord Guild
        Returns: A Row containing the found role, None if none are found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_roles WHERE role_id=?"
        cursor.execute(sql, (role_id,))
        role = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return role

    def add_guild_role(self, role_id: int, guild_id: int, role_type: str):
        """Add a role under a guild role category
        Args:
            role_id: The ID of the role from the Discord Guild
            guild_id: The ID of the Discord Guild the role is in
            role_type: The category of this role (e.g. ADMIN, NEW, VERIFIED etc.)"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_roles (role_id, guild_id, type) VALUES (?, ?, ?)"
        cursor.execute(sql, (role_id, guild_id, role_type))
        self.db_connection.commit_and_close(connection)

    def remove_guild_role(self, role_id: int):
        """Remove a guild role by the role's Discord ID
        Args:
            role_id: The Discord ID of the role to remove"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_roles WHERE role_id=?"
        cursor.execute(sql, (role_id,))
        self.db_connection.commit_and_close(connection)

    def delete_guild_roles(self, guild_id: int):
        """Delete all guild roles of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild roles to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_roles WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_guild_roles_table(self):
        """Delete every single guild role from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_roles"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
