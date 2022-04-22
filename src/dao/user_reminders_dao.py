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

    def get_user_reminders_by_user_id(self, user_id: int):
        """Find all reminders for a given user
        Args:
            user_id: The Discord ID of the user whose reminders to get
        Returns: A list of row objects for the reminders if found, an empty list otherwise"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM user_reminders" \
              "WHERE user_id=?" \
              "INNER JOIN reminders ON user_reminders.reminder_id = reminders.id" \
              "ORDER BY reminders.public ASC, reminders.reminder_date ASC"
        cursor.execute(sql, (user_id,))
        user_reminders = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return user_reminders

    def get_user_reminders_by_reminder_id(self, reminder_id: int):
        """Find all user reminders by the reminder id
        Args:
            reminder_id: The ID of the reminder
        Returns: A list of row objects where the reminder ID matches,
        an empty list if none are found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM user_reminders WHERE reminder_id=?"
        cursor.execute(sql, (reminder_id,))
        user_reminders = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return user_reminders

    def get_all_user_reminders(self):
        """Get all reminders from the database
        Returns: A list of row objects of all the reminders in the database,
        an empty list if there are none"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM user_reminders" \
              "INNER JOIN reminders ON user_reminders.reminder_id = reminders.id" \
              "ORDER BY reminders.public ASC, reminders.reminder_date ASC"
        cursor.execute(sql)
        user_reminders = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return user_reminders

    def create_user_reminder(self, user_id: int, reminder_id: int):
        """Create a new user reminder
        Args:
            user_id: Discord ID of the user this reminder is connected to
            reminder_id: The database ID of the reminder"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO user_reminders (user_id, reminder_id) VALUES (?, ?)"
        cursor.execute(sql, (user_id, reminder_id))
        self.db_connection.commit_and_close(connection)

    def delete_all_by_user_id(self, user_id: int):
        """Delete all reminders tied to a specific user
        Args:
            user_id: Discord ID of the user whose reminders to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders WHERE user_id=?"
        cursor.execute(sql, (user_id,))
        self.db_connection.commit_and_close(connection)

    def delete_all_by_reminder_id(self, reminder_id: int):
        """Delete all instances of a single reminder
        Args:
            reminder_id: Database ID of the reminder whose instances to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM user_reminders WHERE reminder_id=?"
        cursor.execute(sql, (reminder_id,))
        self.db_connection.commit_and_close(connection)
