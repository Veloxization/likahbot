"""Time zones database rows converted into Python objects"""
from entities.master_entity import MasterEntity

class TimeZoneEntity(MasterEntity):
    """An object derived from the time zones database table's rows
    Attributes:
        db_id: The database ID of the time zone
        user_id: The Discord ID of the user to whom the time zone belongs
        time_zone: The user's time zone"""

    def __init__(self, db_id: int, user_id: int, time_zone: str):
        """Create a new TimeZone entity
        Args:
            db_id: The database ID of the time zone
            user_id: The Discord ID of the user to whom the time zone belongs
            time_zone: The user's time zone"""

        self.db_id = db_id
        self.user_id = user_id
        self.time_zone = time_zone
