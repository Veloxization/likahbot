"""The user reminder service is used to call methods in the user reminders DAO class."""

from dao.user_reminders_dao import UserRemindersDAO
from entities.reminder_entity import ReminderEntity
from entities.user_reminder_entity import UserReminderEntity

class UserReminderService:
    """A service for calling methods from user reminders DAO
    Attributes:
        user_reminders_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for user reminders DAO
        Args:
            db_address: The address for the database file where the user reminders table resides"""

        self.user_reminders_dao = UserRemindersDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a user reminder entity
        Args:
            row: The database row to convert to a user reminder entity
        Returns: A user reminder entity equivalent to the database row"""

        if not row:
            return None
        reminder = ReminderEntity(row["reminder_id"], row["creator_id"], row["creator_guild_id"],
                                  row["content"], row["reminder_date"], row["public"],
                                  row["interval"], row["reminder_type"], row["repeats_left"])
        return UserReminderEntity(row["id"], row["user_id"], reminder)

    async def get_user_reminders(self, user_id: int):
        """Get all the reminders the user is opted into
        Args:
            user_id: The Discord ID of the user whose reminders to get
        Returns: A list of UserReminderEntity objects containing the user reminders"""

        rows = await self.user_reminders_dao.get_user_reminders(user_id)
        return [self._convert_to_entity(row) for row in rows]

    async def get_user_reminders_in_guild(self, user_id: int, guild_id: int):
        """Get all the reminders the user is opted into in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to get
            guild_id: The Discord ID of the guild where the reminders are from
        Returns: A list of UserReminderEntity objects containing the user reminders"""

        rows = await self.user_reminders_dao.get_user_reminders_in_guild(user_id, guild_id)
        return [self._convert_to_entity(row) for row in rows]

    async def get_user_reminders_of_reminder_id(self, reminder_id: int):
        """Get all the user reminders linked to a specific reminder
        Args:
            reminder_id: The database ID of the reminder whose linked user reminders to get
        Returns: A list of UserReminderEntity objects containing the found user reminders"""

        rows = await self.user_reminders_dao.get_user_reminders_of_reminder_id(reminder_id)
        return [self._convert_to_entity(row) for row in rows]

    async def get_user_reminder_by_id(self, user_reminder_id: int):
        """Get a specific user reminder by its database ID
        Args:
            user_reminder_id: The database ID of the user reminder to get
        Returns: A UserReminderEntity object containing the found user reminder,
                 None if not found"""

        row = await self.user_reminders_dao.get_user_reminder_by_id(user_reminder_id)
        return self._convert_to_entity(row)

    async def create_user_reminder(self, user_id: int, reminder_id: int):
        """Create a new user reminder
        Args:
            user_id: The Discord ID of the user for whom the reminder is created
            reminder_id: The database ID of the reminder the user opts into
        Returns: A UserReminderEntity object containing the database ID of the newly created
                 user reminder"""

        await self.user_reminders_dao.create_user_reminder(user_id, reminder_id)

    async def delete_user_reminders_of_reminder_id(self, reminder_id: int):
        """Delete all user reminders linked to a specific reminder
        Args:
            reminder_id: The database ID of the reminder whose user opt-ins to delete"""

        await self.user_reminders_dao.delete_user_reminders_of_reminder_id(reminder_id)

    async def delete_user_reminders_of_user(self, user_id: int):
        """Delete all user reminders of a specific user
        Args:
            user_id: The Discord ID of the user whose reminders to delete"""

        await self.user_reminders_dao.delete_user_reminders_of_user(user_id)

    async def delete_user_reminders_of_user_in_guild(self, user_id: int, guild_id: int):
        """Delete all the reminders the user is opted into in a given guild
        Args:
            user_id: The Discord ID of the user whose reminders to delete
            guild_id: The Discord ID of the guild where the reminders are"""

        await self.user_reminders_dao.delete_user_reminders_of_user_in_guild(user_id, guild_id)

    async def delete_user_reminder_by_id(self, user_reminder_id: int):
        """Delete a specific user reminder by its database ID
        Args:
            user_reminder_id: The database ID of the user reminder to delete"""

        await self.user_reminders_dao.delete_user_reminder_by_id(user_reminder_id)

    async def clear_user_reminders(self):
        """Delete every single user reminder"""

        await self.user_reminders_dao.clear_user_reminders_table()
