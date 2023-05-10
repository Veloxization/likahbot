"""The classes and functions handling data access objects for the text_contents table.
The database table keeps track of different text contents the bot may use within a given guild.
Such content may include what the bot says when someone new joins the guild."""
from db_connection.db_connector import DBConnection

class TextContentsDAO:
    """A data access object for text contents
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for text contents
        Args:
            db_address: The address for the database file where the text contents table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_guild_text_contents(self, guild_id: int):
        """Get all text contents for a guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to get
        Returns: A list of Row objects containing the text contents"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM text_contents WHERE guild_id=? ORDER BY content ASC"
        await cursor.execute(sql, (guild_id,))
        text_contents = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return text_contents

    async def get_guild_text_contents_by_type(self, guild_id: int, content_type: str):
        """Get specific text content for a guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to get
            content_type: The type of the text content to find (e.g. WELCOME MESSAGE)
        Returns: A Row object with the text content, if found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM text_contents WHERE guild_id=? AND type=?"
        await cursor.execute(sql, (guild_id, content_type))
        text_content = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return text_content

    async def create_text_content(self, guild_id: int, content: str = None, content_type: str = None):
        """Create new text content for a given guild
        Args:
            guild_id: The Discord ID of the guild this text content belongs to
            content: The actual text content
            content_type: The type of text content (e.g. WELCOME MESSAGE)"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO text_contents (guild_id, content, type) VALUES (?, ?, ?)"
        await cursor.execute(sql, (guild_id, content, content_type))
        await self.db_connection.commit_and_close(connection)

    async def edit_text_content(self, guild_id: int, content_type: str, content: str = None):
        """Edit existing text contents for a given guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to edit
            content_type: The type of text content to edit (e.g. WELCOME MESSAGE)
            content: The content to change to"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE text_contents SET content=? WHERE guild_id=? AND type=?"
        await cursor.execute(sql, (content, guild_id, content_type))
        await self.db_connection.commit_and_close(connection)

    async def delete_text_content(self, guild_id: int, content_type: str):
        """Delete specific text content from a given guild
        Args:
            guild_id: The Discord ID of the guild whose text content to delete
            content_type: The type of text content to delete (e.g. WELCOME MESSAGE)"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM text_contents WHERE guild_id=? AND type=?"
        await cursor.execute(sql, (guild_id, content_type))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_text_contents(self, guild_id: int):
        """Delete all text contents for a given guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM text_contents WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_text_contents_table(self):
        """Delete every single text content from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM text_contents"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
