"""The unverified reminder message service is used to call methods in the unverified reminder
messages DAO class."""

from dao.unverified_reminder_messages_dao import UnverifiedReminderMessagesDAO
from entities.unverified_reminder_message_entity import UnverifiedReminderMessageEntity

class UnverifiedReminderMessageService:
    """A service for calling methods from unverified reminder messages DAO
    Attributes:
        unverified_reminder_messages_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for unverified reminder messages DAO
        Args:
            db_address: The address for the database file where the unverified reminder messages
                        table resides"""

        self.unverified_reminder_messages_dao = UnverifiedReminderMessagesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to an unverified reminder message entity
        Args:
            row: The database row to convert to an unverified reminder message entity
        Returns: An unverified reminder message entity equivalent to the database row"""

        return UnverifiedReminderMessageEntity(row["id"], row["guild_id"], row["message"],
                                               row["timedelta"])

    def get_guild_unverified_reminder_messages(self, guild_id: int):
        """Get all unverified reminder messages for a given guild
        Args:
            guild_id: The Discord ID of the guild whose reminder messages to get
        Returns: A list of unverified reminder message entities"""

        rows = self.unverified_reminder_messages_dao.get_guild_unverified_reminder_messages(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_all_unverified_reminder_messages(self):
        """Get all unverified reminder messages regardless of guild
        Returns: A list of unverified reminder message entities"""

        rows = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        return [self._convert_to_entity(row) for row in rows]

    def add_guild_unverified_reminder_message(self, guild_id: int, message: str, send_time: int):
        """Add a new unverified reminder message for a guild.
        Args:
            guild_id: The Discord ID of the guild this message will be associated with
            message: The message that will be sent to the unverified member
            send_time: The time in seconds that a user has to remain unverified
                       before this message is sent"""

        self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(guild_id,
                                                                                    message,
                                                                                    send_time)

    def edit_guild_unverified_message(self, reminder_message_id: int, message: str, send_time: int):
        """Edit an existing unverified reminder message
        Args:
            reminder_message_id: The database ID of the reminder message to edit
            message: The new message that will be sent to the unverified member
            send_time: The new time the message will be sent after, in seconds"""

        self.unverified_reminder_messages_dao.edit_guild_unverified_message(reminder_message_id,
                                                                            message, send_time)

    def delete_unverified_reminder_message(self, reminder_message_id: int):
        """Delete a specific unverified reminder message
        Args:
            reminder_message_id: The database ID of the message to delete"""

        self.unverified_reminder_messages_dao.delete_unverified_reminder_message(reminder_message_id)

    def delete_guild_reminder_messages(self, guild_id: int):
        """Delete all unverified reminder messages associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose reminder messages to delete"""

        self.unverified_reminder_messages_dao.delete_guild_reminder_messages(guild_id)

    def clear_unverified_reminder_messages(self):
        """Delete every single unverified reminder message"""

        self.unverified_reminder_messages_dao.clear_unverified_reminder_messages_table()
