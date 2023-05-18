"""The classes and functions handling data access objects for the user_reminders table"""
from db_connection.db_connector import DBConnection

class UserRemindersDAO:
    """A data access object for user reminders
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for user reminders
        Args:
            db_address: The address for the database file where the user reminders table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_user_reminders(self, user_id: int):
        """Get all the reminders the user is opted into
        Args:
            user_id: The Discord ID of the user whose reminders to get
        Returns: A list of Row object containing the user reminders"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT ur.id, ur.user_id, ur.reminder_id, r.creator_id, r.creator_guild_id, " \
              "r.content, r.reminder_date, r.public, r.interval, r.reminder_type, r.repeats_left " \
              "FROM user_reminders AS ur LEFT JOIN reminders AS r ON r.id=ur.reminder_id " \
              "WHERE ur.user_id=? ORDER BY r.reminder_date ASC"
        await cursor.execute(sql, (user_id,))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def get_user_reminders_in_guild(self, user_id: int, guild_id: int):
        """Get all the reminders the user is opted into in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to get
            guild_id: The Discord ID of the guild where the reminders are from
        Returns: A list of Row objects containing the user reminders"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT ur.id, ur.user_id, ur.reminder_id, r.creator_id, r.creator_guild_id, " \
              "r.content, r.reminder_date, r.public, r.interval, r.reminder_type, r.repeats_left " \
              "FROM user_reminders AS ur LEFT JOIN reminders AS r ON r.id=ur.reminder_id " \
              "WHERE ur.user_id=? AND r.creator_guild_id=? ORDER BY r.reminder_date ASC"
        await cursor.execute(sql, (user_id, guild_id))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def get_user_reminders_of_reminder_id(self, reminder_id: int):
        """Get all the user reminders linked to a specific reminder
        Args:
            reminder_id: The database ID of the reminder whose linked user reminders to get
        Returns: A list of Row object containing the found user reminders"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT ur.id, ur.user_id, ur.reminder_id, r.creator_id, r.creator_guild_id, " \
              "r.content, r.reminder_date, r.public, r.interval, r.reminder_type, r.repeats_left " \
              "FROM user_reminders AS ur LEFT JOIN reminders AS r ON r.id=ur.reminder_id " \
              "WHERE ur.reminder_id=?"
        await cursor.execute(sql, (reminder_id,))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def get_user_reminder_by_id(self, user_reminder_id: int):
        """Get a specific user reminder by its database ID
        Args:
            user_reminder_id: The database ID of the user reminder to get
        Returns: A Row object containing the found user reminder, None if not found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT ur.id, ur.user_id, ur.reminder_id, r.creator_id, r.creator_guild_id, " \
              "r.content, r.reminder_date, r.public, r.interval, r.reminder_type, r.repeats_left " \
              "FROM user_reminders AS ur LEFT JOIN reminders AS r ON r.id=ur.reminder_id " \
              "WHERE ur.id=?"
        await cursor.execute(sql, (user_reminder_id,))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def create_user_reminder(self, user_id: int, reminder_id: int):
        """Create a new user reminder
        Args:
            user_id: The Discord ID of the user for whom the reminder is created
            reminder_id: The database ID of the reminder the user opts into
        Returns: A Row object containing the database ID of the newly created user reminder"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO user_reminders (user_id, reminder_id) VALUES (?, ?) RETURNING id"
        await cursor.execute(sql, (user_id, reminder_id))
        row = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return row

    async def delete_user_reminders_of_reminder_id(self, reminder_id: int):
        """Delete all user reminders linked to a specific reminder
        Args:
            reminder_id: The database ID of the reminder whose user opt-ins to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders WHERE reminder_id=?"
        await cursor.execute(sql, (reminder_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_reminders_of_user(self, user_id: int):
        """Delete all user reminders of a specific user
        Args:
            user_id: The Discord ID of the user whose reminders to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_reminders_of_user_in_guild(self, user_id: int, guild_id: int):
        """Delete all the reminders the user is opted into in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to delete
            guild_id: The Discord ID of the guild where the reminders are"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders WHERE user_id=? " \
              "AND reminder_id IN (SELECT id FROM reminders WHERE creator_guild_id=?)"
        await cursor.execute(sql, (user_id, guild_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_reminder_by_id(self, user_reminder_id: int):
        """Delete a specific user reminder by its database ID
        Args:
            user_reminder_id: The database ID of the user reminder to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders WHERE id=?"
        await cursor.execute(sql, (user_reminder_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_user_reminders_table(self):
        """Delete every single user reminder from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
