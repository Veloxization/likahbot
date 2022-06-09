"""Text content database rows converted into Python objects"""

class TextContentEntity():
    """An object derived from the text contents database table's rows
    Attributes:
        db_id: The database ID of the text content
        guild_id: The Discord ID of the guild the text content belongs to
        content: The text content itself
        content_type: The type of content, e.g. WELCOME TEXT"""

    def __init__(self, db_id: int, guild_id: int, content: str, content_type: str):
        """Create a new text content entity
        Args:
            db_id: The database ID of the text content
            guild_id: The Discord ID of the guild the text content belongs to
            content: The text content itself
            content_type: The type of content, e.g. WELCOME TEXT"""

        self.db_id = db_id
        self.guild_id = guild_id
        self.content = content
        self.content_type = content_type
