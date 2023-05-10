"""The time zone service is used to call methods in the time zones DAO class."""

from dao.time_zones_dao import TimeZonesDAO
from entities.time_zone_entity import TimeZoneEntity

class TimeZoneService:
    """A service for calling methods from time zones DAO
    Attributes:
        time_zones_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for time zones DAO
        Args:
            db_address: The address for the database file where the time zones table resides"""

        self.time_zones_dao = TimeZonesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a username entity
        Args:
            row: The database row to convert to a username entity
        Returns: A username entity equivalent to the database row"""

        if not row:
            return None
        return TimeZoneEntity(row["id"], row["user_id"], row["time_zone"])

    async def get_user_time_zone(self, user_id: int):
        """Get a user's time zone
        Args:
            user_id: The Discord ID of the user whose time zone to get
        Returns: A TimeZoneEntity containing the user's time zone information. Defaults to UTC."""

        row = await self.time_zones_dao.get_user_time_zone(user_id)
        return self._convert_to_entity(row)

    async def get_time_zone_by_id(self, time_zone_id: int):
        """Get a time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to get
        Returns: A TimeZoneEntity containing the time zone information. None if not found."""

        row = await self.time_zones_dao.get_time_zone_by_id(time_zone_id)
        return self._convert_to_entity(row)

    async def add_user_time_zone(self, user_id: int, time_zone: str = "UTC"):
        """Add a new time zone for a user
        Args:
            user_id: The Discord ID of the user whose time zone to add
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC.
        Returns: The database ID of the newly created time zone"""

        row = await self.time_zones_dao.add_user_time_zone(user_id, time_zone)
        return row["id"]

    async def edit_user_time_zone(self, user_id: int, time_zone: str = "UTC"):
        """Edit an existing user time zone
        Args:
            user_id: The Discord ID of the user whose time zone to edit
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC."""

        await self.time_zones_dao.edit_user_time_zone(user_id, time_zone)

    async def edit_time_zone_by_id(self, time_zone_id: int, time_zone: str = "UTC"):
        """Edit an existing time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to edit
            time_zone: IANA time zone database compatible representation of time zone.
                       Defaults to UTC."""

        await self.time_zones_dao.edit_time_zone_by_id(time_zone_id, time_zone)

    async def delete_user_time_zone(self, user_id: int):
        """Delete the time zone associated with a user
        Args:
            user_id: The Discord ID of the user whose time zone to delete"""

        await self.time_zones_dao.delete_user_time_zone(user_id)

    async def delete_time_zone_by_id(self, time_zone_id: int):
        """Delete a time zone by its database ID
        Args:
            time_zone_id: The database ID of the time zone to delete"""

        await self.time_zones_dao.delete_time_zone_by_id(time_zone_id)

    async def clear_time_zones(self):
        """Delete every single user time zone record"""

        await self.time_zones_dao.clear_time_zones_table()
