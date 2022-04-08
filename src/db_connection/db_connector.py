"""Houses the class used to control database connections."""
import sqlite3

class DBConnection:
    """A class for controlling database connections
    Attributes:
        db_address: The location of the database"""

    def __init__(self, db_address: str):
        """Create a new object for controlling database connections.
        Args:
            db_address: The location of the database"""

        self.db_address = db_address

    def connect_to_db(self):
        """Make a new connection to a database
        Returns: A Connection object and a Cursor object for database commands"""

        connection = sqlite3.connect(self.db_address)
        return connection, connection.cursor()

    def close_connection(self, connection: sqlite3.Connection):
        """Close the connection to a database without commiting changes
        Args:
            connection: The database connection to close"""

        connection.close()

    def commit_changes(self, connection: sqlite3.Connection):
        """Commit changes without closing the connection
        Args:
            connection: The database connection to commit changes to"""

        connection.commit()

    def commit_and_close(self, connection: sqlite3.Connection):
        """Close the connection and commit the changes
        Args:
            connection: The database connection to close"""

        self.commit_changes(connection)
        self.close_connection(connection)
