"""The unverified reminder history service is used to call methods in the utility channels DAO
class."""

from dao.unverified_reminder_history_dao import UnverifiedReminderHistoryDAO
from entities.unverified_reminder_history_entity import UnverifiedReminderHistoryEntity

class UnverifiedReminderHistoryService:
    """A service for calling methods from unverified reminder history DAO
    Attributes:
        unverified_reminder_history_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for unverified reminder history DAO
        Args:
            db_address: The address for the database file where the unverified reminder history
                        table resides"""

        self.unverified_reminder_history_dao = UnverifiedReminderHistoryDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to an unverified reminder history entity
        Args:
            row: The database row to convert to an unverified reminder history entity
        Returns: An unverified reminder history entity equivalent to the database row"""

        return UnverifiedReminderHistoryEntity(row["id"], row["reminder_message_id"],
                                               row["user_id"])

    def get_member_reminder_history(self, user_id: int, guild_id: int):
        """Get all unverified reminders a certain user has received from a specified guild
        Args:
            user_id: The Discord ID of the user whose reminder history to get
            guild_id: The Discord ID of the guild from where the reminders were sent
        Returns: A list of unverified reminder history entities"""

        rows = self.unverified_reminder_history_dao.get_member_reminder_history(user_id, guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def add_to_member_reminder_history(self, user_id: int, reminder_id: int):
        """Add a reminder message to an unverified user's reminder history, marking it as sent
        Args:
            user_id: The Discord ID of the user to whom the verification reminder was sent
            reminder_id: The database ID of the reminder message that was sent"""

        self.unverified_reminder_history_dao.add_to_member_reminder_history(user_id, reminder_id)

    def delete_member_reminder_history(self, user_id: int, guild_id: int):
        """Delete the entire reminder message history of a user from a given guild
        Args:
            user_id: The Discord ID of the user whose reminder message history to delete
            guild_id: The Discord ID of the guild from which the reminders were sent"""

        self.unverified_reminder_history_dao.delete_member_reminder_history(user_id, guild_id)

    def delete_guild_reminder_history(self, guild_id: int):
        """Delete the entire reminder message history associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose reminder message history to delete"""

        self.unverified_reminder_history_dao.delete_guild_reminder_history(guild_id)

    def clear_unverified_reminder_history(self):
        """Delete every single unverified reminder history record"""

        self.unverified_reminder_history_dao.clear_unverified_reminder_history_table()
