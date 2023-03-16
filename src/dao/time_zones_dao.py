"""The classes and functions handling data access objects for the time zones table."""
from db_connection.db_connector import DBConnection

class TimeZonesDAO:
    """A data access object for time zones
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for time zones
        Args:
            db_address: The address for the database file where the time_zones table resides"""

        self.db_connection = DBConnection(db_address)

    def get_user_time_zone(self, user_id: int):
        """Get a user's time zone
        Args:
            user_id: The Discord ID of the user whose time zone to get
        Returns: A Row object containing the user's time zone. Defaults to UTC if not found."""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM time_zones WHERE user_id=?"
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        if not row:
            sql = "SELECT NULL AS id, ? AS user_id, 'UTC' AS time_zone"
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return row

    def get_time_zone_by_id(self, time_zone_id: int):
        """Get a time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to get
        Returns: A Row object containing the time zone. None if not found."""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM time_zones WHERE id=?"
        cursor.execute(sql, (time_zone_id,))
        row = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return row

    def add_user_time_zone(self, user_id: int, time_zone: str = "UTC"):
        """Add a new time zone for a user
        Args:
            user_id: The Discord ID of the user whose time zone to add
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC.
        Returns: A Row object containing the database ID of the newly created user time zone"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO time_zones (user_id, time_zone) VALUES (?, ?) RETURNING id"
        cursor.execute(sql, (user_id, time_zone))
        row = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return row

    def edit_user_time_zone(self, user_id: int, time_zone: str = "UTC"):
        """Edit an existing user time zone
        Args:
            user_id: The Discord ID of the user whose time zone to edit
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC."""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE time_zones SET time_zone=? WHERE user_id=?"
        cursor.execute(sql, (time_zone, user_id))
        self.db_connection.commit_and_close(connection)

    def edit_time_zone_by_id(self, time_zone_id: int, time_zone: str = "UTC"):
        """Edit an existing time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to edit
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC."""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE time_zones SET time_zone=? WHERE id=?"
        cursor.execute(sql, (time_zone, time_zone_id))
        self.db_connection.commit_and_close(connection)

    def delete_user_time_zone(self, user_id: int):
        """Delete the time zone associated with a user
        Args:
            user_id: The Discord ID of the user whose time zone to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM time_zones WHERE user_id=?"
        cursor.execute(sql, (user_id,))
        self.db_connection.commit_and_close(connection)

    def delete_time_zone_by_id(self, time_zone_id: int):
        """Delete a time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM time_zones WHERE id=?"
        cursor.execute(sql, (time_zone_id,))
        self.db_connection.commit_and_close(connection)

    def clear_time_zones_table(self):
        """Delete every single user time zone from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM time_zones"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
