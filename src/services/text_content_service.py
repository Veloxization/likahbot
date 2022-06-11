"""The text content service is used to call methods in the text contents DAO class."""

from dao.text_contents_dao import TextContentsDAO
from entities.text_content_entity import TextContentEntity

class TextContentService:
    """A service for calling methods from text contents DAO
    Attributes:
        text_contents_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for text contents DAO
        Args:
            db_address: The address for the database file where the text contents table resides"""

        self.text_contents_dao = TextContentsDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a text content entity
        Args:
            row: The database row to convert to a text content entity
        Returns: A text content entity equivalent to the database row"""

        return TextContentEntity(row["id"], row["guild_id"], row["content"], row["type"])

    def get_guild_text_contents(self, guild_id: int):
        """Get all text contents for a guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to get
        Returns: A list of text content entities"""

        rows = self.text_contents_dao.get_guild_text_contents(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_guild_text_contents_by_type(self, guild_id: int, content_type: str):
        """Get specific text content for a guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to get
            content_type: The type of the text content to find (e.g. WELCOME MESSAGE)
        Returns: A text content entity, if text content is found"""

        row = self.text_contents_dao.get_guild_text_contents_by_type(guild_id, content_type)
        return self._convert_to_entity(row)

    def create_text_content(self, guild_id: int, content: str = None, content_type: str = None):
        """Create new text content for a given guild
        Args:
            guild_id: The Discord ID of the guild this text content belongs to
            content: The actual text content
            content_type: The type of text content (e.g. WELCOME MESSAGE)"""

        self.text_contents_dao.create_text_content(guild_id, content, content_type)

    def edit_text_content(self, guild_id: int, content_type: str, content: str = None):
        """Edit existing text contents for a given guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to edit
            content_type: The type of text content to edit (e.g. WELCOME MESSAGE)
            content: The content to change to"""

        self.text_contents_dao.edit_text_content(guild_id, content_type, content)

    def delete_text_content(self, guild_id: int, content_type: str):
        """Delete specific text content from a given guild
        Args:
            guild_id: The Discord ID of the guild whose text content to delete
            content_type: The type of text content to delete (e.g. WELCOME MESSAGE)"""

        self.text_contents_dao.delete_text_content(guild_id, content_type)

    def delete_guild_text_contents(self, guild_id: int):
        """Delete all text contents for a given guild
        Args:
            guild_id: The Discord ID of the guild whose text contents to delete"""

        self.text_contents_dao.delete_guild_text_contents(guild_id)

    def clear_text_contents(self):
        """Delete all text contents"""

        self.text_contents_dao.clear_text_contents_table()
