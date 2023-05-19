"""The classes and functions handling data access objects for the guild_settings table"""
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
        sql = "SELECT * FROM guild_settings WHERE id=?"
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
        sql = "SELECT gs.id, gs.guild_id, gs.setting_id, gs.setting_value "\
              "FROM guild_settings AS gs "\
              "LEFT JOIN settings AS s ON setting_id=s.id WHERE guild_id=? AND s.name=?"
        await cursor.execute(sql, (guild_id, setting_name))
        row = await cursor.fetchone()
        if not row:
            sql = "SELECT NULL as id, ? AS guild_id, settings.id AS setting_id, setting_value "\
                  "FROM settings WHERE name=?"
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
        sql = "SELECT * FROM guild_settings WHERE guild_id=? AND setting_id=?"
        await cursor.execute(sql, (guild_id, setting_id))
        row = await cursor.fetchone()
        if not row:
            sql = "SELECT NULL AS id, ? AS guild_id, settings.id AS setting_id, setting_value "\
                  "FROM settings WHERE settings.id=?"
            await cursor.execute(sql, (guild_id, setting_id))
            row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

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
