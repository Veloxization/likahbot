"""The classes and functions handling data access objects for the guild_settings table.
Guild settings are the guild-specific values of the defaults set in the settings table.
They contain values such as what the bot will log on the guild."""
from db_connection.db_connector import DBConnection
from dao.settings_dao import SettingsDAO

class GuildSettingsDAO:
    """A data access object for guild settings
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for guild settings
        Args:
            db_address: The address for the database file where the guild settings table resides"""

        self.db_connection = DBConnection(db_address)
        self.settings_dao = SettingsDAO(db_address)

    async def get_guild_setting_value_by_id(self, guild_setting_id: int):
        """Get a guild setting by its database ID
        Args:
            guild_setting_id: The database ID of the guild setting
        Returns: A Row object containing the guild setting status, None if not found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT gs.*, s.name FROM guild_settings AS gs "\
              "LEFT JOIN settings AS s ON gs.setting_id = s.id WHERE gs.id=?"
        await cursor.execute(sql, (guild_setting_id,))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def get_guild_setting_value_by_name(self, guild_id: int, setting_name: str):
        """Get a guild setting by its name
        Args:
            guild_id: The Discord ID of the guild whose setting to get
            setting_name: The name of the setting to get
        Returns: A Row object containing the setting status, or None if not found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT gs.*, s.name FROM guild_settings AS gs "\
              "LEFT JOIN settings AS s ON setting_id=s.id WHERE guild_id=? AND s.name=?"
        await cursor.execute(sql, (guild_id, setting_name))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def get_guild_setting_value_by_setting_id(self, guild_id: int, setting_id: int):
        """Get a guild setting by the setting ID associated with it
        Args:
            guild_id: The Discord ID of the guild whose setting to get
            setting_id: The database ID of the setting to get (from the settings table)
        Returns: A Row object containing the setting status, None if not found"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT gs.*, s.name FROM guild_settings AS gs "\
              "LEFT JOIN settings AS s ON gs.setting_id = s.id "\
              "WHERE gs.guild_id=? AND gs.setting_id=?"
        await cursor.execute(sql, (guild_id, setting_id))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def get_all_guild_settings(self, guild_id: int):
        """Get all guild settings of a given guild
        Args:
            guild_id: The Discord ID of the guild whose guild settings to get
        Returns: A list of Row objects containing the guild settings of the given guild"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT gs.*, s.name FROM guild_settings AS gs "\
              "LEFT JOIN settings AS s ON gs.setting_id = s.id "\
              "WHERE gs.guild_id=?"
        await cursor.execute(sql, (guild_id,))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def search_guild_settings(self, guild_id: int, keyword: str):
        """Get a list of guild settings based on a keyword
        Args:
            guild_id: The Discord ID of the guild whose settings to get
            keyword: The keyword to search guild settings with
        Returns: A list of Row objects containing the found guild settings"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT gs.*, s.name FROM guild_settings AS gs "\
              "LEFT JOIN settings AS s ON setting_id=s.id WHERE guild_id=? AND s.name LIKE ?"
        await cursor.execute(sql, (guild_id, "%"+keyword+"%"))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def initialize_guild_settings(self, guild_id: int):
        """Create the guild settings for a given guild
        Args:
            guild_id: The Discord ID of the guild whose settings to initialize
        Returns: A list of Row objects containing the IDs of the newly created guild settings"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_settings (guild_id, setting_id, setting_value) "\
              "SELECT (?), id, setting_value FROM settings WHERE id NOT IN "\
              "(SELECT setting_id FROM guild_settings WHERE guild_id=?) "\
              "RETURNING id"
        await cursor.execute(sql, (guild_id, guild_id))
        rows = await cursor.fetchall()
        await self.db_connection.commit_and_close(connection)
        return rows

    async def add_guild_setting_by_setting_id(self, guild_id: int, setting_id: int,
                                              setting_value: str):
        """Add a new guild setting by a setting ID
        Args:
            guild_id: The Discord ID of the guild to add the setting to
            setting_id: The database ID of the setting from the settings table
            setting_value: The value to set the setting to
        Returns: A Row object containing the ID of the newly created guild setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_settings (guild_id, setting_id, setting_value) VALUES (?, ?, ?) "\
              "RETURNING id"
        await cursor.execute(sql, (guild_id, setting_id, setting_value))
        row = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return row

    async def add_guild_setting_by_setting_name(self,
        guild_id: int,
        setting_name: str,
        setting_value: str):
        """Add a new guild setting by a setting name
        Args:
            guild_id: The Discord ID of the guild to add the setting to
            setting_name: The name of the setting to add to the guild
            setting_value: The value to set the setting to
        Returns: A Row object containing the ID of the newly created guild setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_settings (guild_id, setting_id, setting_value) "\
              "VALUES (?, (SELECT id FROM settings WHERE name=?), ?) RETURNING id"
        await cursor.execute(sql, (guild_id, setting_name, setting_value))
        row = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return row

    async def edit_guild_setting_by_id(self, guild_setting_id: int, setting_value: str):
        """Edit a guild setting by its ID
        Args:
            guild_setting_id: The database ID of the guild setting to edit
            setting_value: The value to change to"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_value=? WHERE id=?"
        await cursor.execute(sql, (setting_value, guild_setting_id))
        await self.db_connection.commit_and_close(connection)

    async def edit_guild_setting_by_setting_id(self, guild_id: int, setting_id: int,
                                               setting_value: str):
        """Edit a guild setting by the setting's ID
        Args:
            guild_id: The Discord ID of the guild whose setting to edit
            setting_id: The database ID of the setting from the settings table
            setting_value: The value to change to"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_value=? WHERE guild_id=? AND setting_id=?"
        await cursor.execute(sql, (setting_value, guild_id, setting_id))
        await self.db_connection.commit_and_close(connection)

    async def edit_guild_setting_by_setting_name(self,
        guild_id: int,
        setting_name: str,
        setting_value: str):
        """Edit a guild setting by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to edit
            setting_name: The name of the setting
            setting_value: The value to change to"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_value=? WHERE guild_id=? "\
              "AND setting_id=(SELECT id FROM settings WHERE name=?)"
        await cursor.execute(sql, (setting_value, guild_id, setting_name))
        await self.db_connection.commit_and_close(connection)

    async def edit_guild_settings_by_setting_name_pattern(self,
        guild_id: int,
        setting_name_pattern: str,
        setting_value: str):
        """Edit all guild settings with a certain name pattern within a guild to a certain value
        Args:
            guild_id: The Discord ID of the guild whose settings to edit
            setting_name_pattern: The pattern of setting names which need to be changed
            setting_value: The value to change the settings to"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_value=? WHERE guild_id=? AND setting_id IN "\
              "(SELECT id FROM settings WHERE name LIKE ?)"
        await cursor.execute(sql, (setting_value, guild_id, "%"+setting_name_pattern+"%"))
        await self.db_connection.commit_and_close(connection)

    async def reset_guild_setting_to_default_value(self, guild_id: int, guild_setting_id: int):
        """Return a guild setting back to its default value as defined in the settings table
        Args:
            guild_id: The Discord ID of the guild whose setting to reset
            guild_setting_id: The database ID of the guild setting to reset"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_value=(SELECT setting_value FROM settings "\
              "WHERE id=(SELECT setting_id FROM guild_settings WHERE guild_id=? AND id=?)) "\
              "WHERE guild_id=? AND setting_id=?"
        await cursor.execute(sql, (guild_id, guild_setting_id, guild_id, guild_setting_id))
        await self.db_connection.commit_and_close(connection)

    async def reset_guild_setting_to_default_value_by_name(self, guild_id: int, setting_name: str):
        """Return a guild setting back to its default value as defined by the settings table,
        by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to reset
            setting_name: The name of the setting to reset"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_value=(SELECT setting_value FROM settings "\
              "WHERE name=?) WHERE guild_id=? AND setting_id=(SELECT id FROM settings "\
              "WHERE name=?)"
        await cursor.execute(sql, (setting_name, guild_id, setting_name))
        await self.db_connection.commit_and_close(connection)

    async def reset_all_guild_settings_to_default_value(self, guild_id: int):
        """Reset all guild settings within a guild into their default values as defined in the
        settings table
        Args:
            guild_id: The Discord ID of the guild whose settings to reset"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings AS gs SET setting_value="\
              "(SELECT setting_value FROM settings AS s WHERE s.id=gs.setting_id) "\
              "WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_setting_by_id(self, guild_setting_id: int):
        """Delete a guild setting by its ID
        Args:
            guild_setting_id: The database ID of the guild setting to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE id=?"
        await cursor.execute(sql, (guild_setting_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_setting_by_setting_id(self, guild_id: int, setting_id: int):
        """Delete a guild setting by the setting's ID
        Args:
            guild_id: The Discord ID of the guild whose setting to delete
            setting_id: The database ID of the setting corresponding to the guild setting to
                        delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE guild_id=? AND setting_id=?"
        await cursor.execute(sql, (guild_id, setting_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_setting_by_setting_name(self, guild_id: int, setting_name: str):
        """Delete a guild setting by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to delete
            setting_name: The name of the setting to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE guild_id=? "\
              "AND setting_id=(SELECT id FROM settings WHERE name=?)"
        await cursor.execute(sql, (guild_id, setting_name))
        await self.db_connection.commit_and_close(connection)

    async def delete_guild_settings(self, guild_id: int):
        """Delete all settings associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose settings to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE guild_id=?"
        await cursor.execute(sql, (guild_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_guild_settings_table(self):
        """Delete every single guild setting from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
