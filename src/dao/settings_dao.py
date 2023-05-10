"""The classes and functions handling data access objects for the settings table"""
from db_connection.db_connector import DBConnection

class SettingsDAO:
    """A data access object for settings
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for settings
        Args:
            db_address: The address for the database file where the settings table resides"""

        self.db_connection = DBConnection(db_address)

    async def get_setting_default_value(self, setting_name: str):
        """Get a setting of a given name
        Args:
            setting_name: The name of the setting
        Returns: A Row object containing the default value of the given setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM settings WHERE name=?"
        await cursor.execute(sql, (setting_name,))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def get_setting_default_value_by_id(self, setting_id: int):
        """Get a setting of a given id
        Args:
            setting_id: The database ID of the setting to get
        Returns: A Row object containing the default value of the given setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM settings WHERE id=?"
        await cursor.execute(sql, (setting_id,))
        row = await cursor.fetchone()
        await self.db_connection.close_connection(connection)
        return row

    async def add_setting(self, setting_name: str, default_value: str):
        """Create a new setting with a default value
        This is only for consistency. Most default settings will be added through schema.
        Args:
            setting_name: The name of the setting to add
            default_value: The default value of the setting
        Returns: A Row object with the ID of the newly created setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO settings (name, setting_value) VALUES (?, ?) RETURNING id"
        await cursor.execute(sql, (setting_name, default_value))
        row = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return row

    async def edit_setting_default_by_name(self, setting_name: str, default_value: str):
        """Edit a setting by its name
        Args:
            setting_name: The name of the setting to edit
            default_value: The new default status for the setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE settings SET setting_value=? WHERE name=?"
        await cursor.execute(sql, (default_value, setting_name))
        await self.db_connection.commit_and_close(connection)

    async def edit_setting_default_by_id(self, setting_id: int, default_value: str):
        """Edit a setting by its id
        Args:
            setting_id: The database ID of the setting to edit
            default_value: The new default status for the setting"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "UPDATE settings SET setting_value=? WHERE id=?"
        await cursor.execute(sql, (default_value, setting_id))
        await self.db_connection.commit_and_close(connection)

    async def delete_setting_by_name(self, setting_name: str):
        """Delete a setting by its name
        Args:
            setting_name: The name of the setting to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM settings WHERE name=?"
        await cursor.execute(sql, (setting_name,))
        await self.db_connection.commit_and_close(connection)

    async def delete_setting_by_id(self, setting_id: int):
        """Delete a setting by its id
        Args:
            setting_id: The database ID of the setting to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM settings WHERE id=?"
        await cursor.execute(sql, (setting_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_settings_table(self):
        """Delete every single setting from the table"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM settings"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
