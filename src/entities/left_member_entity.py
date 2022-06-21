"""Left member database rows converted into Python objects"""

from time_handler.time import TimeStringConverter
from entities.master_entity import MasterEntity

class LeftMemberEntity(MasterEntity):
    """An object derived from the left members database table's rows
    Attributes:
        db_id: The database ID of the left member
        user_id: The Discord ID of the left member
        guild_id: The Discord ID of the guild the member left from
        leave_date: A datetime object telling the time the member left"""

    def __init__(self, db_id: int, user_id: int, guild_id: int, leave_date: str):
        """Create a new left member entity
        Args:
            db_id: The database ID of the left member
            user_id: The Discord ID of the left member
            guild_id: The Discord ID of the guild the member left from
            leave_date: A string telling the time the member left"""

        self.db_id = db_id
        self.user_id = user_id
        self.guild_id = guild_id
        converter = TimeStringConverter()
        self.leave_date = converter.string_to_datetime(leave_date)
