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

    def get_guild_setting_status_by_id(self, guild_setting_id: int):
        """Get a guild setting by its database ID
        Args:
            guild_setting_id: The database ID of the guild setting
        Returns: A Row object containing the guild setting status, None if not found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT setting_status FROM guild_settings WHERE id=?"
        cursor.execute(sql, (guild_setting_id,))
        row = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return row

    def get_guild_setting_status_by_name(self, guild_id: int, setting_name: str):
        """Get a guild setting by its name
        Args:
            guild_id: The Discord ID of the guild whose setting to get
            setting_name: The name of the setting to get
        Returns: A Row object containing the setting status, or None if not found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT setting_status FROM guild_settings "\
              "LEFT JOIN settings AS s ON setting_id=s.id WHERE guild_id=? AND s.name=?"
        cursor.execute(sql, (guild_id, setting_name))
        row = cursor.fetchone()
        if not row:
            self.settings_dao.get_setting_default_value(setting_name)
        self.db_connection.close_connection(connection)
        return row

    def get_guild_setting_status_by_setting_id(self, guild_id: int, setting_id: int):
        """Get a guild setting by the setting ID associated with it
        Args:
            guild_id: The Discord ID of the guild whose setting to get
            setting_id: The database ID of the setting to get (from the settings table)
        Returns: A Row object containing the setting status, None if not found"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT setting_status FROM guild_settings WHERE guild_id=? AND setting_id=?"
        cursor.execute(sql, (guild_id, setting_id))
        row = cursor.fetchone()
        if not row:
            row = self.settings_dao.get_setting_default_value_by_id(setting_id)
        self.db_connection.close_connection(connection)
        return row

    def add_guild_setting_by_setting_id(self, guild_id: int, setting_id: int, setting_status: str):
        """Add a new guild setting by a setting ID
        Args:
            guild_id: The Discord ID of the guild to add the setting to
            setting_id: The database ID of the setting from the settings table
            setting_status: The status to set the setting to
        Returns: A Row object containing the ID of the newly created guild setting"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_settings (guild_id, setting_id, setting_status) VALUES (?, ?, ?) "\
              "RETURNING id"
        cursor.execute(sql, (guild_id, setting_id, setting_status))
        row = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return row

    def add_guild_setting_by_setting_name(self,
        guild_id: int,
        setting_name: str,
        setting_status: str):
        """Add a new guild setting by a setting name
        Args:
            guild_id: The Discord ID of the guild to add the setting to
            setting_name: The name of the setting to add to the guild
            setting_status: The status to set the setting to
        Returns: A Row object containing the ID of the newly created guild setting"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO guild_settings (guild_id, setting_id, setting_status) "\
              "VALUES (?, (SELECT id FROM settings WHERE name=?), ?) RETURNING id"
        cursor.execute(sql, (guild_id, setting_name, setting_status))
        row = cursor.fetchone()
        self.db_connection.commit_and_close(connection)
        return row

    def edit_guild_setting_by_id(self, guild_setting_id: int, setting_status: str):
        """Edit a guild setting by its ID
        Args:
            guild_setting_id: The database ID of the guild setting to edit
            setting_status: The value to change the status to"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_status=? WHERE id=?"
        cursor.execute(sql, (setting_status, guild_setting_id))
        self.db_connection.commit_and_close(connection)

    def edit_guild_setting_by_setting_id(self, guild_id: int, setting_id: int, setting_status: str):
        """Edit a guild setting by the setting's ID
        Args:
            guild_id: The Discord ID of the guild whose setting to edit
            setting_id: The database ID of the setting from the settings table
            setting_status: The value to change the status to"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_status=? WHERE guild_id=? AND setting_id=?"
        cursor.execute(sql, (setting_status, guild_id, setting_id))
        self.db_connection.commit_and_close(connection)

    def edit_guild_setting_by_setting_name(self,
        guild_id: int,
        setting_name: str,
        setting_status: str):
        """Edit a guild setting by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to edit
            setting_name: The name of the setting
            setting_status: The value to change the status to"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "UPDATE guild_settings SET setting_status=? WHERE guild_id=? "\
              "AND setting_id=(SELECT id FROM settings WHERE name=?)"
        cursor.execute(sql, (setting_status, guild_id, setting_name))
        self.db_connection.commit_and_close(connection)

    def delete_guild_setting_by_id(self, guild_setting_id: int):
        """Delete a guild setting by its ID
        Args:
            guild_setting_id: The database ID of the guild setting to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE id=?"
        cursor.execute(sql, (guild_setting_id,))
        self.db_connection.commit_and_close(connection)

    def delete_guild_setting_by_setting_id(self, guild_id: int, setting_id: int):
        """Delete a guild setting by the setting's ID
        Args:
            guild_id: The Discord ID of the guild whose setting to delete
            setting_id: The database ID of the setting corresponding to the guild setting to
                        delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE guild_id=? AND setting_id=?"
        cursor.execute(sql, (guild_id, setting_id))
        self.db_connection.commit_and_close(connection)

    def delete_guild_setting_by_setting_name(self, guild_id: int, setting_name: str):
        """Delete a guild setting by the setting's name
        Args:
            guild_id: The Discord ID of the guild whose setting to delete
            setting_name: The name of the setting to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE guild_id=? "\
              "AND setting_id=(SELECT id FROM settings WHERE name=?)"
        cursor.execute(sql, (guild_id, setting_name))
        self.db_connection.commit_and_close(connection)

    def delete_guild_settings(self, guild_id: int):
        """Delete all settings associated with a given guild
        Args:
            guild_id: The Discord ID of the guild whose settings to delete"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings WHERE guild_id=?"
        cursor.execute(sql, (guild_id,))
        self.db_connection.commit_and_close(connection)

    def clear_guild_settings_table(self):
        """Delete every single guild setting from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM guild_settings"
        cursor.execute(sql)
        self.db_connection.commit_and_close(connection)
