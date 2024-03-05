"""The guild setting service is used to call methods in the guild settings DAO class."""
from dao.guild_settings_dao import GuildSettingsDAO
from entities.setting_entity import SettingEntity
from entities.guild_setting_entity import GuildSettingEntity

class GuildSettingService:
    """A service for calling methods from guild settings DAO
    Attributes:
        guild_settings_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for guild settings DAO
        Args:
            db_address: The address for the database file where the guild settings table resides"""

        self.guild_settings_dao = GuildSettingsDAO(db_address)

    def _convert_to_entity(self, row):
        """Covert a database row into a guild setting entity
        Args:
            row: The database row to convert to a guild setting entity
        Returns: A guild setting entity equivalent to the database row"""

        if not row:
            return None
        setting = SettingEntity(row["setting_id"], row["name"], row["setting_value"])
        return GuildSettingEntity(row["id"], row["guild_id"], setting,
                                  row["setting_value"])

    async def get_guild_setting_value_by_id(self, guild_setting_id: int):
        """Get a guild setting by its database ID
        Args:
            guild_setting_id: The database ID of the guild setting
        Returns: A guild setting entity containing the guild setting status, None if not found"""

        row = await self.guild_settings_dao.get_guild_setting_value_by_id(guild_setting_id)
        return self._convert_to_entity(row)

    async def get_guild_setting_value_by_name(self, guild_id: int, setting_name: str):
        """Get a guild setting by its name
        Args:
            guild_id: The Discord ID of the guild whose setting to get
            setting_name: The name of the setting to get
        Returns: A guild setting entity containing the setting status, or None if not found"""

        row = await self.guild_settings_dao.get_guild_setting_value_by_name(guild_id, setting_name)
        return self._convert_to_entity(row)

    async def get_guild_setting_value_by_setting_id(self, guild_id: int, setting_id: int):
        """Get a guild setting by the setting ID associated with it
        Args:
            guild_id: The Discord ID of the guild whose setting to get
            setting_id: The database ID of the setting to get (from the settings table)
        Returns: A guild setting entity containing the setting status, None if not found"""

        row = await self.guild_settings_dao.get_guild_setting_value_by_setting_id(guild_id,
                                                                                  setting_id)
        return self._convert_to_entity(row)

    async def get_all_guild_settings(self, guild_id: int):
        """Get all guild settings of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild settings to get
        Returns: A list of guild setting entities containing the guild settings of the given
                 guild"""

        rows = await self.guild_settings_dao.get_all_guild_settings(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    async def search_guild_settings(self, guild_id: int, keyword: str):
        """Get a list of guild settings based on a keyword
        Args:
            guild_id: The Discord ID of the guild whose settings to get
            keyword: The keyword to search guild settings with
        Returns: A list of guild setting entities containing the found guild settings"""

        rows = await self.guild_settings_dao.search_guild_settings(guild_id, keyword)
        return [self._convert_to_entity(row) for row in rows]

    async def initialize_guild_settings(self, guild_id: int):
        """Create the guild settings for a given guild
        Args:
            guild_id: The Discord ID of the guild whose settings to initialize
        Returns: A list of database IDs of the newly create guild settings"""

        rows = await self.guild_settings_dao.initialize_guild_settings(guild_id)
        return [row["id"] for row in rows]

    async def add_guild_setting_by_setting_id(self, guild_id: int, setting_id: int,
                                              setting_value: str):
        """Add a new guild setting by a setting ID
        Args:
            guild_id: The Discord ID of the guild to add the setting to
            setting_id: The database ID of the setting from the settings table
            setting_value: The value to set the setting to
        Returns: The database ID of the newly created guild setting"""

        row = await self.guild_settings_dao.add_guild_setting_by_setting_id(guild_id, setting_id,
                                                                            setting_value)
        return row["id"]

    async def add_guild_setting_by_setting_name(self,
        guild_id: int,
        setting_name: str,
        setting_value: str):
        """Add a new guild setting by a setting name
        Args:
            guild_id: The Discord ID of the guild to add the setting to
            setting_name: The name of the setting to add to the guild
            setting_value: The value to set the setting to
        Returns: The database ID of the newly created guild setting"""

        row = await self.guild_settings_dao.add_guild_setting_by_setting_name(guild_id,
                                                                              setting_name,
                                                                              setting_value)
        return row["id"]

    async def edit_guild_setting_by_id(self, guild_setting_id: int, setting_value: str):
        """Edit a guild setting by its ID
        Args:
            guild_setting_id: The database ID of the guild setting to edit
            setting_value: The value to change to"""

        await self.guild_settings_dao.edit_guild_setting_by_id(guild_setting_id, setting_value)

    async def edit_guild_setting_by_setting_id(self, guild_id: int, setting_id: int,
                                               setting_value: str):
        """Edit a guild setting by the setting's ID
        Args:
            guild_id: The Discord ID of the guild whose setting to edit
            setting_id: The database ID of the setting from the settings table
            setting_value: The value to change to"""

        await self.guild_settings_dao.edit_guild_setting_by_setting_id(guild_id, setting_id,
                                                                       setting_value)

    async def edit_guild_setting_by_setting_name(self,
        guild_id: int,
        setting_name: str,
        setting_value: str):
        """Edit a guild setting by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to edit
            setting_name: The name of the setting
            setting_value: The value to change to"""

        await self.guild_settings_dao.edit_guild_setting_by_setting_name(guild_id,
                                                                         setting_name,
                                                                         setting_value)

    async def edit_guild_settings_by_setting_name_pattern(self,
        guild_id: int,
        setting_name_pattern: str,
        setting_value: str):
        """Edit all guild settings with a certain name pattern within a guild to a certain value
        Args:
            guild_id: The Discord ID of the guild whose settings to edit
            setting_name_pattern: The pattern of setting names which need to be changed
            setting_value: The value to change the settings to"""

        await self.guild_settings_dao.edit_guild_settings_by_setting_name_pattern(guild_id,
                                                                                  setting_name_pattern,
                                                                                  setting_value)

    async def reset_guild_setting_to_default_value(self, guild_id: int, guild_setting_id: int):
        """Return a guild setting back to its default value as defined in the settings table
        Args:
            guild_id: The Discord ID of the guild whose setting to reset
            guild_setting_id: The database ID of the guild setting to reset"""

        await self.guild_settings_dao.reset_guild_setting_to_default_value(guild_id,
                                                                           guild_setting_id)

    async def reset_guild_setting_to_default_value_by_name(self, guild_id: int, setting_name: str):
        """Return a guild setting back to its default value as defined by the settings table,
        by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to reset
            setting_name: The name of the setting to reset"""

        await self.guild_settings_dao.reset_guild_setting_to_default_value_by_name(guild_id,
                                                                                   setting_name)

    async def reset_all_guild_settings_to_default_value(self, guild_id: int):
        """Reset all guild settings within a guild into their default values as defined in the
        settings table
        Args:
            guild_id: The Discord ID of the guild whose settings to reset"""

        await self.guild_settings_dao.reset_all_guild_settings_to_default_value(guild_id)

    async def delete_guild_setting_by_id(self, guild_setting_id: int):
        """Delete a guild setting by its ID
        Args:
            guild_setting_id: The database ID of the guild setting to delete"""

        await self.guild_settings_dao.delete_guild_setting_by_id(guild_setting_id)

    async def delete_guild_setting_by_setting_id(self, guild_id: int, setting_id: int):
        """Delete a guild setting by the setting's ID
        Args:
            guild_id: The Discord ID of the guild whose setting to delete
            setting_id: The database ID of the setting corresponding to the guild setting to
                        delete"""

        await self.guild_settings_dao.delete_guild_setting_by_setting_id(guild_id, setting_id)

    async def delete_guild_setting_by_setting_name(self, guild_id: int, setting_name: str):
        """Delete a guild setting by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to delete
            setting_name: The name of the setting to delete"""

        await self.guild_settings_dao.delete_guild_setting_by_setting_name(guild_id, setting_name)

    async def delete_guild_settings(self, guild_id: int):
        """Delete all settings associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose settings to delete"""

        await self.guild_settings_dao.delete_guild_settings(guild_id)

    async def clear_guild_settings(self):
        """Delete every single guild setting"""

        await self.guild_settings_dao.clear_guild_settings_table()
