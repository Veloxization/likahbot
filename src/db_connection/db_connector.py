"""Houses the class used to control database connections."""
import asyncio
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

        retries = 0
        while retries <= 10:
            try:
                connection = await sqlite3.connect(self.db_address)
                break
            except sqlite3.DatabaseError:
                await asyncio.sleep(0.1)
                retries += 1
        if retries > 10:
            raise sqlite3.DatabaseError("Database connection failed")
        connection.row_factory = sqlite3.Row
        cursor = await connection.cursor()
        await cursor.execute("PRAGMA foreign_keys = ON;")
        return connection, cursor

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
