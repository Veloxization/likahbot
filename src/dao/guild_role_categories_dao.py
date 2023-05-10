"""The classes and functions handling data access objects for the guild_role_categories table.
The database table keeps track of the role categories for a given guild. Categories could include
the roles given when a user first joins a server, or when they're a moderator."""
from db_connection.db_connector import DBConnection

class GuildRoleCategoriesDAO():
    """A data access object for guild role categories
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for guild role categories
        Args:
            db_address: The address for the database file where the guild_role_categories table
                        resides"""

        self.db_connection = DBConnection(db_address)

    async def get_all_guild_role_categories(self, guild_id: int):
        """Get all guild role categories of a given guild
        Args:
            guild_id: The Discord ID of the guild whose role categories to get
        Returns: A list of Rows containing the found categories"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM guild_role_categories WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        categories = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return categories

    async def add_guild_role_category(self, guild_id: int, category: str):
        """Add a new guild role category for a given guild
        Args:
            guild_id: The Discord ID of the guild that gets the new category
            category: The type of category, e.g. MODERATOR or ADMIN"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_role_categories (guild_id, category) VALUES (?, ?)"
        await cursor.execute(sql, (guild_id, category))
        await self.db_connection.commit_and_close(connection)

    async def remove_guild_role_category(self, category_id: int):
        """Remove a guild role category by its database ID
        Args:
            category_id: The database ID of the category to remove"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_role_categories WHERE id=?"
        await cursor.execute(sql, (category_id,))
        await self.db_connection.commit_and_close(connection)

    async def remove_all_guild_role_categories(self, guild_id: int):
        """Remove all guild role categories of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild role categories to remove"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_role_categories WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_guild_role_categories_table(self):
        """Delete every single guild role category from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_role_categories"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
