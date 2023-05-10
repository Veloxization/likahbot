"""The setting service is used to call methods in the settings DAO class."""

from dao.settings_dao import SettingsDAO
from entities.setting_entity import SettingEntity

class SettingService:
    """A service for calling methods from settings DAO
    Attributes:
        settings_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for settings DAO
        Args:
            db_address: The address for the database file where the settings table resides"""

        self.settings_dao = SettingsDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a setting entity
        Args:
            row: The database row to convert to a setting entity
        Returns: A setting entity equivalent to the database row"""

        if not row:
            return None
        return SettingEntity(row["id"], row["name"], row["setting_value"])

    async def get_setting_default_value(self, setting_name: str):
        """Get a setting of a given name
        Args:
            setting_name: The name of the setting
        Returns: A Setting entity"""

        row = await self.settings_dao.get_setting_default_value(setting_name)
        return self._convert_to_entity(row)

    async def get_setting_default_value_by_id(self, setting_id: int):
        """Get a setting of a given id
        Args:
            setting_id: The database ID of the setting to get
        Returns: A Setting entity"""

        row = await self.settings_dao.get_setting_default_value_by_id(setting_id)
        return self._convert_to_entity(row)

    async def add_setting(self, setting_name: str, default_value: str):
        """Create a new setting with a default value
        This is only for consistency. Most default settings will be added through schema.
        Args:
            setting_name: The name of the setting to add
            default_value: The default value of the setting
        Returns: The database ID of the newly created setting"""

        row = await self.settings_dao.add_setting(setting_name, default_value)
        return row["id"]

    async def edit_setting_default_by_name(self, setting_name: str, default_value: str):
        """Edit a setting by its name
        Args:
            setting_name: The name of the setting to edit
            default_value: The new default status for the setting"""

        await self.settings_dao.edit_setting_default_by_name(setting_name, default_value)

    async def edit_setting_default_by_id(self, setting_id: int, default_value: str):
        """Edit a setting by its id
        Args:
            setting_id: The database ID of the setting to edit
            default_value: The new default status for the setting"""

        await self.settings_dao.edit_setting_default_by_id(setting_id, default_value)

    async def delete_setting_by_name(self, setting_name: str):
        """Delete a setting by its name
        Args:
            setting_name: The name of the setting to delete"""

        await self.settings_dao.delete_setting_by_name(setting_name)

    async def delete_setting_by_id(self, setting_id: int):
        """Delete a setting by its id
        Args:
            setting_id: The database ID of the setting to delete"""

        await self.settings_dao.delete_setting_by_id(setting_id)

    async def clear_settings(self):
        """Delete every single setting default"""

        await self.settings_dao.clear_settings_table()
