"""The classes and functions handling data access objects for the reminders table"""
from db_connection.db_connector import DBConnection
from datetime import datetime

class RemindersDAO:
    """A data access object for reminders
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for reminders
        Args:
            db_address: The address for the database file where the reminders table resides"""

        self.db_connection = DBConnection(db_address)

    def get_reminders_by_user(self, user_id: int):
        """Get all reminders made by a given user
        Args:
            user_id: The Discord ID of the user whose reminders to get
        Returns: A list of Row objects containing the user's reminders"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE creator_id=? ORDER BY reminder_date ASC"
        cursor.execute(sql, (user_id,))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_public_reminders_by_user(self, user_id: int):
        """Get all public reminders made by a given user
        Args:
            user_id: The Discord ID of the user whose public reminders to get
        Returns: A list of Row objects containing the user's public reminders"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE creator_id=? AND public=TRUE " \
              "ORDER BY reminder_date ASC"
        cursor.execute(sql, (user_id,))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_reminders_by_user_in_guild(self, user_id: int, guild_id: int):
        """Get all reminders made by a given user in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to get
            guild_id: The Discord ID of the guild in which the reminders were created
        Returns: A list of Row objects containing the user's reminders in the guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders " \
              "WHERE creator_id=? AND creator_guild_id=? AND creator_guild_id IS NOT NULL " \
              "ORDER BY reminder_date ASC"
        cursor.execute(sql, (user_id, guild_id))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_public_reminders_by_user_in_guild(self, user_id: int, guild_id: int):
        """Get all public reminders made by a given user in a given guild
        Args:
            user_id: The Discord ID of the user whose public reminders to get
            guild_id: The Discord ID of the guild in which the reminders were created
        Returns: A list of Row objects containing the user's public reminders in the guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders " \
              "WHERE creator_id=? AND creator_guild_id=? AND public=TRUE " \
              "AND creator_guild_id IS NOT NULL " \
              "ORDER BY reminder_date ASC"
        cursor.execute(sql, (user_id, guild_id))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_reminders_in_guild(self, guild_id: int):
        """Get all reminders in a given guild
        Args:
            guild_id: The Discord ID of the guild in which the reminders were created
        Returns: A list of Row objects containing the reminders of the guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE creator_guild_id=? AND creator_guild_id IS NOT NULL " \
              "ORDER BY reminder_date ASC"
        cursor.execute(sql, (guild_id,))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_public_reminders_in_guild(self, guild_id: int):
        """Get all public reminders in a given guild
        Args:
            guild_id: The Discord ID of the guild in which the public reminders were created
        Returns: A list of Row objects containing the public reminders of the guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE creator_guild_id=? AND public=TRUE " \
              "AND creator_guild_id IS NOT NULL " \
              "ORDER BY reminder_date ASC"
        cursor.execute(sql, (guild_id,))
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_expired_reminders(self):
        """Get all reminders that have expired
        Returns: A list of Row objects containing all the expired reminders"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE reminder_date<datetime() ORDER BY reminder_date ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return rows

    def get_reminder_by_id(self, reminder_id: int):
        """Get a reminder by its database ID
        Args:
            reminder_id: The database ID of the reminder to get
        Returns: A Row object containing the found reminder, None if not found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE id=?"
        cursor.execute(sql, (reminder_id,))
        row = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return row

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
        Returns: A Row object containing the database ID of the newly created reminder."""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO reminders (creator_id, creator_guild_id, content, reminder_date, " \
                                     "public, interval, reminder_type, repeats_left) " \
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id"
        cursor.execute(sql, (user_id, guild_id, content, reminder_date, is_public, interval,
                             reminder_type, repeats))
        row = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return row

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

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE reminders SET content=?, reminder_date=?, public=?, interval=?, " \
              "reminder_type=?, repeats_left=? WHERE id=?"
        cursor.execute(sql, (content, reminder_date, is_public, interval, reminder_type, repeats,
                             reminder_id))
        self.db_connection.commit_and_close(connection)

    def update_reminder_repeats(self, reminder_id: int):
        """Update the repeats in a given reminder if it hasn't reached 0. This method will not
           delete a reminder whose repeats fall to 0 so make sure to delete those separately.
        Args:
            reminder_id: The database ID of the reminder whose repeats to update"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE reminders SET repeats_left=repeats_left-1 WHERE id=? AND repeats_left>0"
        cursor.execute(sql, (reminder_id,))
        self.db_connection.commit_and_close(connection)

    def delete_user_reminders(self, user_id: int):
        """Delete all reminders made by a given user
        Args:
            user_id: The Discord ID of the user whose reminders to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders WHERE creator_id=?"
        cursor.execute(sql, (user_id,))
        self.db_connection.commit_and_close(connection)

    def delete_user_reminders_in_guild(self, user_id: int, guild_id: int):
        """Delete all reminders made by a given user in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to delete
            guild_id: The Discord ID of the guild in which the reminders were created"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders WHERE creator_id=? AND creator_guild_id=?"
        cursor.execute(sql, (user_id, guild_id))
        self.db_connection.commit_and_close(connection)

    def delete_guild_reminders(self, guild_id: int):
        """Delete all reminders made in a given guild
        Args:
            guild_id: The Discord ID of the guild in which the reminders were created"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders WHERE creator_guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def delete_reminder_by_id(self, reminder_id: int):
        """Delete a reminder by its database ID
        Args:
            reminder_id: The database ID of the reminder to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders WHERE id=?"
        cursor.execute(sql, (reminder_id,))
        self.db_connection.commit_and_close(connection)

    def delete_reminders_with_no_repeats(self):
        """Delete all reminders that have reached 0 repeats"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders WHERE repeats_left=0"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)

    def clear_reminders_table(self):
        """Delete every single reminder from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
