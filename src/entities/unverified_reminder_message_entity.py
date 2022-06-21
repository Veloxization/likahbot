"""Unverified reminder message database rows converted into Python objects"""

from entities.master_entity import MasterEntity

class UnverifiedReminderMessageEntity(MasterEntity):
    """An object derived from the unverified reminder messages database table's rows
    Attributes:
        db_id: The database ID of the unverified reminder message
        message: The verification reminder message that will be sent to an unverified user
        timedelta: The time in seconds until the message is sent, counted from time of joining"""

    def __init__(self, db_id: int, message: str, timedelta: int):
        """Create a new unverified reminder message entity
        Args:
            db_id: The database ID of the unverified reminder message
            message: The verification reminder message that will be sent to an unverified user
            timedelta: The time in seconds until the message is sent, counted from time of
                       joining"""

        self.db_id = db_id
        self.message = message
        self.timedelta = timedelta
