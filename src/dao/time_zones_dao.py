"""The classes and functions handling data access objects for the time zones table.
Time zones are used to automatically adjust reminders and birthday announcements to the associated
user's time zone."""
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

    async def get_user_time_zone(self, user_id: int):
        """Get a user's time zone
        Args:
            user_id: The Discord ID of the user whose time zone to get
        Returns: A Row object containing the user's time zone. Defaults to UTC if not found."""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM time_zones WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        row = await cursor.fetchone()
        if not row:
            sql = "SELECT NULL AS id, ? AS user_id, 'UTC' AS time_zone"
            await cursor.execute(sql, (user_id,))
            row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def get_time_zone_by_id(self, time_zone_id: int):
        """Get a time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to get
        Returns: A Row object containing the time zone. None if not found."""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM time_zones WHERE id=?"
        await cursor.execute(sql, (time_zone_id,))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def add_user_time_zone(self, user_id: int, time_zone: str = "UTC"):
        """Add a new time zone for a user
        Args:
            user_id: The Discord ID of the user whose time zone to add
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC.
        Returns: A Row object containing the database ID of the newly created user time zone"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO time_zones (user_id, time_zone) VALUES (?, ?) RETURNING id"
        await cursor.execute(sql, (user_id, time_zone))
        row = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return row

    async def edit_user_time_zone(self, user_id: int, time_zone: str = "UTC"):
        """Edit an existing user time zone
        Args:
            user_id: The Discord ID of the user whose time zone to edit
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC."""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE time_zones SET time_zone=? WHERE user_id=?"
        await cursor.execute(sql, (time_zone, user_id))
        await self.db_connection.commit_and_close(connection)

    async def edit_time_zone_by_id(self, time_zone_id: int, time_zone: str = "UTC"):
        """Edit an existing time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to edit
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC."""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE time_zones SET time_zone=? WHERE id=?"
        await cursor.execute(sql, (time_zone, time_zone_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_time_zone(self, user_id: int):
        """Delete the time zone associated with a user
        Args:
            user_id: The Discord ID of the user whose time zone to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM time_zones WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_time_zone_by_id(self, time_zone_id: int):
        """Delete a time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM time_zones WHERE id=?"
        await cursor.execute(sql, (time_zone_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_time_zones_table(self):
        """Delete every single user time zone from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM time_zones"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
