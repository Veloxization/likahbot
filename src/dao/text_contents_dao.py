"""The classes and functions handling data access objects for the text_contents table"""
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

    def get_guild_text_contents(self, guild_id: int):
        """Get all text contents for a guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to get
        Returns: A list of Row objects containing the text contents"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM text_contents WHERE guild_id=? ORDER BY content ASC"
        cursor.execute(sql, (guild_id,))
        text_contents = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return text_contents

    def get_guild_text_contents_by_type(self, guild_id: int, content_type: str):
        """Get specific text content for a guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to get
            content_type: The type of the text content to find (e.g. WELCOME MESSAGE)
        Returns: A Row object with the text content, if found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM text_contents WHERE guild_id=? AND type=?"
        cursor.execute(sql, (guild_id, content_type))
        text_content = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return text_content

    def create_text_content(self, guild_id: int, content: str = None, content_type: str = None):
        """Create new text content for a given guild
        Args:
            guild_id: The Discord ID of the guild this text content belongs to
            content: The actual text content
            content_type: The type of text content (e.g. WELCOME MESSAGE)"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO text_contents (guild_id, content, type) VALUES (?, ?, ?)"
        cursor.execute(sql, (guild_id, content, content_type))
        self.db_connection.commit_and_close(connection)

    def edit_text_content(self, guild_id: int, content_type: str, content: str = None):
        """Edit existing text contents for a given guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to edit
            content_type: The type of text content to edit (e.g. WELCOME MESSAGE)
            content: The content to change to"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE text_contents SET content=? WHERE guild_id=? AND type=?"
        cursor.execute(sql, (content, guild_id, content_type))
        self.db_connection.commit_and_close(connection)

    def delete_text_content(self, guild_id: int, content_type: str):
        """Delete specific text content from a given guild
        Args:
            guild_id: The Discord ID of the guild whose text content to delete
            content_type: The type of text content to delete (e.g. WELCOME MESSAGE)"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM text_contents WHERE guild_id=? AND type=?"
        cursor.execute(sql, (guild_id, content_type))
        self.db_connection.commit_and_close(connection)

    def delete_guild_text_contents(self, guild_id: int):
        """Delete all text contents for a given guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM text_contents WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)
