"""Houses the class used to control database connections."""
import aiosqlite as sqlite3

class DBConnection:
    """A class for controlling database connections
    Attributes:
        db_address: The location of the database"""

    def __init__(self, db_address: str):
        """Create a new object for controlling database connections.
        Args:
            db_address: The location of the database"""

        self.db_address = db_address

    async def connect_to_db(self):
        """Make a new connection to a database
        Returns: A Connection object and a Cursor object for database commands"""

        connection = await sqlite3.connect(self.db_address)
        connection.row_factory = sqlite3.Row
        return connection, await connection.cursor()

    async def close_connection(self, connection: sqlite3.Connection):
        """Close the connection to a database without commiting changes
        Args:
            connection: The database connection to close"""

        await connection.close()

    async def commit_changes(self, connection: sqlite3.Connection):
        """Commit changes without closing the connection
        Args:
            connection: The database connection to commit changes to"""

        await connection.commit()

    async def commit_and_close(self, connection: sqlite3.Connection):
        """Close the connection and commit the changes
        Args:
            connection: The database connection to close"""

        await self.commit_changes(connection)
        await self.close_connection(connection)
