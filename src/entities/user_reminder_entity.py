"""User reminder database rows converted into Python objects"""
from entities.master_entity import MasterEntity
from entities.reminder_entity import ReminderEntity

class UserReminderEntity(MasterEntity):
    """An object derived from the user reminders database table's rows
    Attributes:
        db_id: The database ID of the user reminder
        user_id: The Discord ID of the user whose reminder this is
        reminder: The ReminderEntity object this user reminder relates to"""

    def __init__(self, db_id: int, user_id: int, reminder: ReminderEntity):
        """Create a new Reminder entity
        Args:
            db_id: The database ID of the user reminder
            user_id: The Discord ID of the user whose reminder this is
            reminder: The ReminderEntity object this user reminder relates to"""

        self.db_id = db_id
        self.user_id = user_id
        self.reminder = reminder
