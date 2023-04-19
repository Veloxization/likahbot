"""The reminder service is used to call methods in the reminders DAO class."""

from datetime import datetime
from dao.reminders_dao import RemindersDAO
from entities.reminder_entity import ReminderEntity

class ReminderService:
    """A service for calling methods from reminders DAO
    Attributes:
        reminders_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for reminders DAO
        Args:
            db_address: The address for the database file where the reminders table resides"""

        self.reminders_dao = RemindersDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a reminder entity
        Args:
            row: The database row to convert to a reminder entity
        Returns: A reminder entity equivalent to the database row"""

        if not row:
            return None
        return ReminderEntity(row["id"], row["creator_id"], row["creator_guild_id"],
                              row["content"], row["reminder_date"], row["public"], row["interval"],
                              row["reminder_type"], row["repeats_left"])

    def get_reminders_by_user(self, user_id: int):
        """Get all reminders made by a given user
        Args:
            user_id: The Discord ID of the user whose reminders to get
        Returns: A list of ReminderEntity objects containing the user's reminders"""

        rows = self.reminders_dao.get_reminders_by_user(user_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_public_reminders_by_user(self, user_id: int):
        """Get all public reminders made by a given user
        Args:
            user_id: The Discord ID of the user whose public reminders to get
        Returns: A list of ReminderEntity objects containing the user's public reminders"""

        rows = self.reminders_dao.get_public_reminders_by_user(user_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_reminders_by_user_in_guild(self, user_id: int, guild_id: int):
        """Get all reminders made by a given user in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to get
            guild_id: The Discord ID of the guild in which the reminders were created
        Returns: A list of ReminderEntity objects containing the user's reminders in the guild"""

        rows = self.reminders_dao.get_reminders_by_user_in_guild(user_id, guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_public_reminders_by_user_in_guild(self, user_id: int, guild_id: int):
        """Get all public reminders made by a given user in a given guild
        Args:
            user_id: The Discord ID of the user whose public reminders to get
            guild_id: The Discord ID of the guild in which the reminders were created
        Returns: A list of ReminderEntity objects containing the user's public reminders in the
                 guild"""

        rows = self.reminders_dao.get_public_reminders_by_user_in_guild(user_id, guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_reminders_in_guild(self, guild_id: int):
        """Get all reminders in a given guild
        Args:
            guild_id: The Discord ID of the guild in which the reminders were created
        Returns: A list of ReminderEntity objects containing the reminders of the guild"""

        rows = self.reminders_dao.get_reminders_in_guild(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_public_reminders_in_guild(self, guild_id: int):
        """Get all public reminders in a given guild
        Args:
            guild_id: The Discord ID of the guild in which the public reminders were created
        Returns: A list of ReminderEntity objects containing the public reminders of the guild"""

        rows = self.reminders_dao.get_public_reminders_in_guild(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_expired_reminders(self):
        """Get all reminders that have expired
        Returns: A list of ReminderEntity objects containing all the expired reminders"""

        rows = self.reminders_dao.get_expired_reminders()
        return [self._convert_to_entity(row) for row in rows]

    def get_reminder_by_id(self, reminder_id: int):
        """Get a reminder by its database ID
        Args:
            reminder_id: The database ID of the reminder to get
        Returns: A ReminderEntity object containing the found reminder, None if not found"""

        row = self.reminders_dao.get_reminder_by_id(reminder_id)
        return self._convert_to_entity(row)

    def add_new_reminder(self, user_id: int, guild_id: int, content: str, reminder_date: datetime,
                         reminder_type: str, is_public: bool = False, interval: int = 0,
                         repeats: int = 1):
        """Create a new reminder
        Args:
            user_id: The Discord ID of the user creating the reminder
            guild_id: The Discord ID of the guild the reminder is being created in
            content: The content of the reminder (what it's reminding about)
            reminder_date: The date when the reminder will expire and the reminders will be sent out
            is_public: Whether users other than the creator can opt in to get reminded,
                       defaults to False
            interval: How often the reminder repeats, in seconds. Defaults to 60.
            reminder_type: The type of the reminder. Can be weekday, day, time or after.
            repeats: How many times the reminder repeats before getting deleted. Defaults to 1.
        Returns: The database ID of the newly created reminder."""

        return self.reminders_dao.add_new_reminder(user_id, guild_id, content, reminder_date,
                                                   reminder_type, is_public, interval, 
                                                   repeats)["id"]

    def edit_reminder(self, reminder_id: int, content: str, reminder_date: datetime,
                      is_public: bool, interval: int, reminder_type: str, repeats: int):
        """Edit an existing reminder
        Args:
            reminder_id: The database ID of the reminder to edit
            content: The new content of the reminder
            reminder_date: The new expiration date for the reminder
            is_public: Whether this reminder is pubic
            interval: How often the reminder repeats, in seconds
            repeats: How many times the reminder repeats before getting deleted"""

        self.reminders_dao.edit_reminder(reminder_id, content, reminder_date, is_public, interval,
                                         reminder_type, repeats)

    def update_reminder_repeats(self, reminder_id: int):
        """Update the repeats in a given reminder if it hasn't reached 0. This method will not
           delete a reminder whose repeats fall to 0 so make sure to delete those separately.
        Args:
            reminder_id: The database ID of the reminder whose repeats to update"""

        self.reminders_dao.update_reminder_repeats(reminder_id)

    def delete_user_reminders(self, user_id: int):
        """Delete all reminders made by a given user
        Args:
            user_id: The Discord ID of the user whose reminders to delete"""

        self.reminders_dao.delete_user_reminders(user_id)

    def delete_user_reminders_in_guild(self, user_id: int, guild_id: int):
        """Delete all reminders made by a given user in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to delete
            guild_id: The Discord ID of the guild in which the reminders were created"""

        self.reminders_dao.delete_user_reminders_in_guild(user_id, guild_id)

    def delete_guild_reminders(self, guild_id: int):
        """Delete all reminders made in a given guild
        Args:
            guild_id: The Discord ID of the guild in which the reminders were created"""

        self.reminders_dao.delete_guild_reminders(guild_id)

    def delete_reminder_by_id(self, reminder_id: int):
        """Delete a reminder by its database ID
        Args:
            reminder_id: The database ID of the reminder to delete"""

        self.reminders_dao.delete_reminder_by_id(reminder_id)

    def delete_reminders_with_no_repeats(self):
        """Delete all reminders that have reached 0 repeats"""

        self.reminders_dao.delete_reminders_with_no_repeats()

    def clear_reminders(self):
        """Delete every single reminder"""

        self.reminders_dao.clear_reminders_table()
