"""Unverified reminder history database rows converted into Python objects"""

from entities.master_entity import MasterEntity

class UnverifiedReminderHistoryEntity(MasterEntity):
    """An object derived from the unverified reminder history database table's rows
    Attributes:
        db_id: The database ID of the unverified reminder history entry
        reminder_message_id: The database ID of the sent reminder message
        user_id: The Discord ID of the user to whom the reminder was sent"""

    def __init__(self, db_id: int, reminder_message_id: int, user_id: int):
        """Create a new unverified reminder history entity
        Args:
            db_id: The database ID of the unverified reminder history
            reminder_message_id: The database ID of the sent reminder message
            user_id: The Discord ID of the user to whom the reminder was sent"""

        self.db_id = db_id
        self.reminder_message_id = reminder_message_id
        self.user_id = user_id
