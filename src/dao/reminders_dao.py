"""The classes and functions handling data access objects for the reminders table"""
from datetime import datetime
from db_connection.db_connector import DBConnection
from time_handler.time import TimeStringConverter

class RemindersDAO:
    """A data access object for reminders
    Attributes:
        db_connection: An object that handles database connections
        time_convert: An object that handles conversion between datetime and string"""

    def __init__(self, db_address, time_string_format="%Y-%m-%d %H:%M:%S"):
        """Create a new data access object for reminders
        Args:
            db_address: The address for the database file where the reminders table resides
            time_string_format: The format to convert datetime to string and vice versa"""

        self.db_connection = DBConnection(db_address)
        self.time_convert = TimeStringConverter(time_string_format)

    def get_all_reminders(self):
        """Get all the reminders
        Returns: A list of Rows containing all reminders"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders ORDER BY reminder_date"
        cursor.execute(sql)
        reminders = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return reminders

    def get_reminder(self, reminder_id: int):
        """Get a specific reminder
        Args:
            reminder_id: The database ID of the reminder to get
        Returns: A Row object containing the info of the reminder, None if not found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM reminders WHERE id=?"
        cursor.execute(sql, (reminder_id,))
        reminder = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return reminder

    def create_reminder(self, content: str, reminder_date: datetime, public: bool,
                        interval: int = None, repeats: int = None, next_reminder: str = None):
        """Create a new reminder
        Args:
            content: The content of the reminder
            reminder_date: The date when the reminder next triggers
            public: Whether the reminder is publicly visible or for a specific user
            interval: The interval at which the reminder will repeat, in milliseconds
            repeats: The number of times this reminder will repeat
            next_reminder: The string to parse the next values for a new reminder
        Returns: A Row object containing the reminder that was just created"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO reminders" \
              "(content, reminder_date, public, interval, repeats_left, next_reminder) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        reminder_date = self.time_convert.datetime_to_string(reminder_date)
        cursor.execute(sql, (content, reminder_date, public, interval, repeats, next_reminder))
        sql = "SELECT last_insert_rowid()"
        cursor.execute(sql)
        reminder_id = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return self.get_reminder(reminder_id)

    def delete_reminder(self, reminder_id: int):
        """Delete a reminder
        Args:
            reminder_id: The ID of the reminder to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM reminders WHERE id=?"
        cursor.execute(sql, (reminder_id,))
        self.db_connection.commit_and_close(connection)
