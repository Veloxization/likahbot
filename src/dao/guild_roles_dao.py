"""The classes and functions handling data access objects for the guild_roles table.
The database table keeps track of roles used for varying purposes within a guild.
A guild may have a separate role for new members, verified new members, full members,
admins and moderators, for example."""
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
        """Get all guild roles of a specified Guild
        Args:
            guild_id: The ID of the Discord Guild to look for roles
        Returns:
            A list of Rows containing the found roles"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_roles " \
              "INNER JOIN guild_role_categories AS grc ON category_id=grc.id" \
              "WHERE guild_id=? ORDER BY category ASC"
        cursor.execute(sql, (guild_id,))
        roles = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return roles

    def get_guild_roles_of_type(self, role_category: str, guild_id: int):
        """Get all Guild roles of specific type
        Args:
            role_category: The category of role to get (e.g. ADMIN, NEW, VERIFIED etc.)
            guild_id: The ID of the Discord Guild to look for roles
        Returns:
            A list of Rows containing the found roles"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_roles " \
              "INNER JOIN guild_role_categories AS grc ON category_id=grc.id " \
              "WHERE category=? AND guild_id=?"
        cursor.execute(sql, (role_category, guild_id))
        roles = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return roles

    def get_guild_roles_by_role_id(self, role_id: int):
        """Get guild roles with a specific ID
        Args:
            role_id: The ID of the role from the Discord Guild
        Returns: A list of Rows containing the found roles"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_roles " \
              "INNER JOIN guild_role_categories AS grc ON category_id=grc.id " \
              "WHERE role_id=?"
        cursor.execute(sql, (role_id,))
        roles = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return roles

    def add_guild_role(self, role_id: int, category_id: int):
        """Add a role under a guild role category
        Args:
            role_id: The ID of the role from the Discord Guild
            category_id: The database ID of the category this role belongs in"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_roles (role_id, category_id) VALUES (?, ?)"
        cursor.execute(sql, (role_id, category_id))
        self.db_connection.commit_and_close(connection)

    def remove_guild_role_from_category(self, role_id: int, category_id: int):
        """Remove a guild role by the role's Discord ID
        Args:
            role_id: The Discord ID of the role to remove
            category_id: The database ID of the category to remove this role from"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_roles WHERE role_id=? AND category_id=?"
        cursor.execute(sql, (role_id, category_id))
        self.db_connection.commit_and_close(connection)

    def delete_guild_roles(self, guild_id: int):
        """Delete all guild roles of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild roles to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_roles WHERE category_id IN " \
              "(SELECT id FROM guild_role_categories WHERE guild_id=?)"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_guild_roles_table(self):
        """Delete every single guild role from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_roles"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
