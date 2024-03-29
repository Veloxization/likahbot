"""The classes and functions handling data access objects for the unverified reminder history
table.
The database table keeps track of verification reminders already sent to the user and is
linked to the unverified_reminder_messages table. This way the bot doesn't accidentally
send the same reminder twice to the same user."""
from db_connection.db_connector import DBConnection

class UnverifiedReminderHistoryDAO:
    """A data access object for unverified reminder history
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for unverified reminder history
        Args:
            db_address: The address for the database file where the unverified reminder history
                        table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_member_reminder_history(self, user_id: int, guild_id: int):
        """Get all unverified reminders a certain user has received from a specified guild
        Args:
            user_id: The Discord ID of the user whose reminder history to get
            guild_id: The Discord ID of the guild from where the reminders were sent
        Returns: A list of Rows containing the member's reminder history"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT urh.id, reminder_message_id, user_id " \
              "FROM unverified_reminder_history AS urh " \
              "INNER JOIN unverified_reminder_messages AS urm ON urm.id=reminder_message_id " \
              "WHERE user_id=? AND guild_id=? " \
              "ORDER BY timedelta DESC"
        await cursor.execute(sql, (user_id, guild_id))
        message_history = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return message_history

    async def add_to_member_reminder_history(self, user_id: int, reminder_id: int):
        """Add a reminder message to an unverified user's reminder history, marking it as sent
        Args:
            user_id: The Discord ID of the user to whom the verification reminder was sent
            reminder_id: The database ID of the reminder message that was sent"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO unverified_reminder_history (reminder_message_id, user_id) " \
              "VALUES (?, ?)"
        await cursor.execute(sql, (reminder_id, user_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_member_reminder_history(self, user_id: int, guild_id: int):
        """Delete the entire reminder message history of a user from a given guild
        Args:
            user_id: The Discord ID of the user whose reminder message history to delete
            guild_id: The Discord ID of the guild from which the reminders were sent"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_reminder_history AS urh WHERE user_id=? AND urh.id IN " \
              "(SELECT urh.id FROM unverified_reminder_history AS urh " \
              "INNER JOIN unverified_reminder_messages AS urm ON urm.id=reminder_message_id " \
              "WHERE guild_id=?)"
        await cursor.execute(sql, (user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_reminder_history(self, guild_id: int):
        """Delete the entire reminder message history associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose reminder message history to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_reminder_history AS urh WHERE urh.id IN " \
              "(SELECT urh.id FROM unverified_reminder_history AS urh " \
              "INNER JOIN unverified_reminder_messages AS urm ON urm.id=reminder_message_id " \
              "WHERE guild_id=?)"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_unverified_reminder_history_table(self):
        """Delete every single unverified reminder history from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_reminder_history"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
