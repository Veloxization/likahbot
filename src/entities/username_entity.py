"""Username database rows converted into Python objects"""

from time_handler.time import TimeStringConverter
from entities.master_entity import MasterEntity

class UsernameEntity(MasterEntity):
    """An object derived from the usernames database table's rows
    Attributes:
        db_id: The database ID of the username
        user_id: The Discord ID of the user this username is tied to
        username: The username string
        time: A datetime object telling the time this username came to be used"""

    def __init__(self, db_id: int, user_id: int, username: str, time: str):
        """Create a new Username entity
        Args:
            db_id: The database ID of the username
            user_id: The Discord ID of the user this username is tied to
            username: The username string
            time: The time string telling the time this username came to be used"""

        self.db_id = db_id
        self.user_id = user_id
        self.username = username
        converter = TimeStringConverter()
        self.time = converter.string_to_datetime(time)
