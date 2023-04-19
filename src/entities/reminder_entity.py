"""Reminder database rows converted into Python objects"""
from entities.master_entity import MasterEntity

class ReminderEntity(MasterEntity):
    """An object derived from the reminders database table's rows
    Attributes:
        db_id: The database ID of the reminder
        user_id: The Discord ID of the user who created the reminder
        guild_id: The Discord ID of the guild in which the reminder was created
        content: The content of the reminder
        reminder_date: The date when the reminder will expire, represented as a string
        is_public: Whether the reminder is public, i.e. can other people in the guild opt in
        interval: How often the reminder repeats, in seconds
        reminder_type: The type of reminder. Options: weekday, date, time, after
        repeats_left: How many times the reminder will repeat before being deleted.
                      A value of -1 means repeated until manually deleted."""

    def __init__(self, db_id: int, user_id: int, guild_id: int, content: str, reminder_date: str,
                 is_public: bool, interval: int, reminder_type: str, repeats_left: int):
        """Create a new Reminder entity
        Args:
            db_id: The database ID of the reminder
            user_id: The Discord ID of the user who created the reminder
            guild_id: The Discord ID of the guild in which the reminder was created
            content: The content of the reminder
            reminder_date: The date when the reminder will expire, represented as a string
            is_public: Whether the reminder is public, i.e. can other people in the guild opt in
            interval: How often the reminder repeats, in seconds
            reminder_type: The type of reminder. Options: weekday, date, time, after
            repeats_left: How many times the reminder will repeat before being deleted.
                          A value of -1 means repeated until manually deleted."""

        self.db_id = db_id
        self.user_id = user_id
        self.guild_id = guild_id
        self.content = content
        self.reminder_date = reminder_date
        self.is_public = is_public
        self.interval = interval
        self.reminder_type = reminder_type
        self.repeats_left = repeats_left
