"""The classes and functions handling data access objects for the global names table.
The database table keeps track of the history of a user's global names, i.e. the one displayed
above the username."""
from db_connection.db_connector import DBConnection

class GlobalNamesDAO:
    """A data access object for global names
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for global names
        Args:
            db_address: The address for the database file where the global_names table resides"""

        self.db_connection = DBConnection(db_address)

    async def _delete_earlier_global_names(self, user_id: int, global_name_id: int):
        """Delete the global_name_id global name and all global names registered before it
        Args:
            user_id: The Discord ID of the user whose global names to delete
            global_name_id: The database ID of the global name used as a reference point for
                            deletion"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM global_names WHERE user_id=? "\
              "AND time<=(SELECT time FROM global_names WHERE id=?)"
        await cursor.execute(sql, (user_id, global_name_id))
        await self.db_connection.commit_and_close(connection)

    async def find_global_names(self, global_name: str):
        """Find all instances of a given global name in the database
        Args:
            global_name: The global name to find in the database
        Returns: A list of Row objects containing the found global names"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM global_names WHERE global_name=?"
        await cursor.execute(sql, (global_name,))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def find_user_global_names(self, user_id: int):
        """Find all global names of a given user
        Args:
            user_id: The Discord ID of the user whose global names to find
        Returns: A list of Row objects containing the user's saved global name history"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "SELECT * FROM global_names WHERE user_id=? ORDER BY time DESC"
        await cursor.execute(sql, (user_id,))
        rows = await cursor.fetchall()
        await self.db_connection.close_connection(connection)
        return rows

    async def add_global_name(self, global_name: str, user_id: int, global_name_limit: int = 5):
        """Add a new global name to the database. If more than limit names exist already,
           the oldest are deleted.
        Args:
            global_name: The username to add
            user_id: The Discord ID of the user this global name is associated with
            global_name_limit: How many global names for one user are allowed in the database
                               at a time
        Returns: The database ID of the newly created global name"""

        previous_global_names = await self.find_user_global_names(user_id)
        if len(previous_global_names) >= global_name_limit:
            this_username = previous_global_names.pop(0)
            await self._delete_earlier_global_names(user_id, this_username["id"])

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "INSERT INTO global_names (user_id, global_name, time) "\
              "VALUES (?, ?, datetime()) RETURNING id"
        await cursor.execute(sql, (user_id, global_name))
        row = await cursor.fetchone()
        await self.db_connection.commit_and_close(connection)
        return row["id"]

    async def delete_global_name(self, global_name_id: int):
        """Delete a global name by its database ID
        Args:
            global_name_id: The database ID of the global name to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM global_names WHERE id=?"
        await cursor.execute(sql, (global_name_id,))
        await self.db_connection.commit_and_close(connection)

    async def delete_user_global_names(self, user_id: int):
        """Delete all saved global names of a given user
        Args:
            user_id: The Discord ID of the user whose global names to delete"""

        connection, cursor = await self.db_connection.connect_to_db()
        sql = "DELETE FROM global_names WHERE user_id=?"
        await cursor.execute(sql, (user_id,))
        await self.db_connection.commit_and_close(connection)

    async def clear_global_names_table(self):
        """Delete every single global name from the table"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM global_names"
        await cursor.execute(sql)
        await self.db_connection.commit_and_close(connection)
