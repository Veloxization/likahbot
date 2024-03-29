"""The classes and functions handling data access objects for the unverified reminder messages
table.
The database table keeps track of the reminder messages sent to joining members about verification.
If a guild uses bot verification and a member doesn't go through with it in a timely manner, these
reminders can help the user remember to verify."""
from db_connection.db_connector import DBConnection

class UnverifiedReminderMessagesDAO:
    """A data access object for unverified reminder messages
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for unverified reminder messages
        Args:
            db_address: The address for the database file where the unverified reminder messages
                        table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_guild_unverified_reminder_messages(self, guild_id: int):
        """Get all unverified reminder messages for a given guild
        Args:
            guild_id: The Discord ID of the guild whose reminder messages to get
        Returns: A list of Rows containing the message and its time interval"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT id, message, timedelta FROM unverified_reminder_messages WHERE guild_id=? " \
              "ORDER BY timedelta ASC"
        await cursor.execute(sql, (guild_id,))
        messages = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return messages

    async def get_all_unverified_reminder_messages(self):
        """Get all unverified reminder messages regardless of guild
        Returns: A list of Rows containing the message data"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM unverified_reminder_messages ORDER BY guild_id ASC, timedelta ASC"
        await cursor.execute(sql)
        messages = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return messages

    async def add_guild_unverified_reminder_message(self, guild_id: int, message: str, send_time: int):
        """Add a new unverified reminder message for a guild.
        Args:
            guild_id: The Discord ID of the guild this message will be associated with
            message: The message that will be sent to the unverified member
            send_time: The time in seconds that a user has to remain unverified
                       before this message is sent"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO unverified_reminder_messages (guild_id, message, timedelta) " \
              "VALUES (?, ?, ?)"
        await cursor.execute(sql, (guild_id, message, send_time))
        await self.db_connection.commit_and_close(connection)

    async def edit_guild_unverified_message(self, reminder_message_id: int, message: str, send_time: int):
        """Edit an existing unverified reminder message
        Args:
            reminder_message_id: The database ID of the reminder message to edit
            message: The new message that will be sent to the unverified member
            send_time: The new time the message will be sent after, in seconds"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE unverified_reminder_messages SET message=?, timedelta=? WHERE id=?"
        await cursor.execute(sql, (message, send_time, reminder_message_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_unverified_reminder_message(self, reminder_message_id: int):
        """Delete a specific unverified reminder message
        Args:
            reminder_message_id: The database ID of the message to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_reminder_messages WHERE id=?"
        await cursor.execute(sql, (reminder_message_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_reminder_messages(self, guild_id: int):
        """Delete all unverified reminder messages associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose reminder messages to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_reminder_messages WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_unverified_reminder_messages_table(self):
        """Delete every single unverified reminder message from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM unverified_reminder_messages"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
