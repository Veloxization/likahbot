"""The classes and functions handling data access objects for the experience table"""
from datetime import datetime
from db_connection.db_connector import DBConnection
from time_handler.time import TimeStringConverter, TimeDifference

class ExperienceDAO:
    """A data access object for experience
    Attributes:
        db_connection: An object that handles database connections
        time_convert: An object that handles conversion between datetime and string"""

    def __init__(self, db_address, time_string_format="%Y-%m-%d %H:%M:%S"):
        """Create a new data access object for experience
        Args:
            db_address: The address for the database file where the experience table resides
            time_string_format: The format to convert datetime to string and vice versa"""

        self.db_connection = DBConnection(db_address)
        self.time_convert = TimeStringConverter(time_string_format)

    def get_server_leaderboard(self, server_id: int):
        """Get all experience in a Guild
        Args:
            server_id: The ID of the Guild whose experience points to list
        Returns: A list of Rows containing the experience points of the selected Guild"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM experience WHERE server_id=? ORDER BY amount DESC"
        cursor.execute(sql, (server_id,))
        experience = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return experience

    def get_user_experience(self, user_id: int, server_id: int):
        """Get the experience for a specific user on a specific Guild
        Args:
            user_id: The user whose experience to get
            server_id: The ID of the Guild from which to get the experience
        Returns: A single Row with the user experience, None if no experience is found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM experience WHERE user_id=? AND server_id=?"
        cursor.execute(sql, (user_id, server_id))
        experience = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return experience

    def add_user_experience(self, user_id: int, server_id: int, amount: int,
                            time: datetime, interval: int):
        """Give the user of a specific guild a specific amount of experience.
        Experience will not be awarded if time to last_experience is less than the specified
        interval.
        Args:
            user_id: The Discord ID of the user who gets the experience
            server_id: The ID of the Guild on which the experience is awarded
            amount: The amount of experience to award
            time: The current time
            interval: The interval, in milliseconds, after which the user is eligible for more
                      experience"""

        experience = self.get_user_experience(user_id, server_id)
        connection, cursor = self.db_connection.connect_to_db()
        if not experience:
            sql = "INSERT INTO experience (user_id, server_id, last_experience, amount) \
                   VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (user_id, server_id, time, amount))
        else:
            last_experience = self.time_convert.string_to_datetime(experience["last_experience"])
            time_difference = TimeDifference().time_difference_ms(time, last_experience)
            if time_difference > interval:
                sql = "UPDATE experience SET amount=amount+? WHERE user_id=? AND server_id=?"
                cursor.execute(sql, (amount, user_id, server_id))
        self.db_connection.commit_and_close(connection)

    def reset_user_experience(self, user_id: int, server_id: int):
        """Reset a user's experience in a Guild back to 0
        Args:
            user_id: The Discord ID of the user whose experience to reset
            server_id: The ID of the guild in which the experience is reset"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE experience SET amount=0, last_experience=NULL WHERE user_id=? AND server_id=?"
        cursor.execute(sql, (user_id, server_id))
        self.db_connection.commit_and_close(connection)

    def delete_user_experience(self, user_id: int, server_id: int):
        """Delete the database entry for a user's experience
        Args:
            user_id: The Discord ID of the user whose experience to delete
            server_id: The ID of the guild from which to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM experience WHERE user_id=? AND server_id=?"
        cursor.execute(sql, (user_id, server_id))
        self.db_connection.commit_and_close(connection)
