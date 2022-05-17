"""The classes and functions handling data access objects for the left members table"""
from db_connection.db_connector import DBConnection

class LeftMembersDAO:
    """A data access object for left members
    Attributes:
        db_connection: An object that handles database connections"""

    def __init__(self, db_address):
        """Create a new data access object for left members
        Args:
            db_address: The address for the database file where the left members table resides"""

        self.db_connection = DBConnection(db_address)

    def get_all_guild_left_members(self, guild_id: int):
        """Find all members who have left the specified guild
        Args:
            guild_id: The Discord ID of the guild whose left members to get
        Returns: A list of Rows containing data on left members"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM left_members WHERE guild_id=? ORDER BY leave_date ASC"
        cursor.execute(sql, (guild_id,))
        members = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return members

    def get_all_left_members(self):
        """Find all members who have left any guild the bot is in
        Returns: A list of Rows containing data on left members"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM left_members ORDER BY leave_date ASC"
        cursor.execute(sql)
        members = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return members

    def get_guild_left_member(self, user_id: int, guild_id: int):
        """Find a specific member who has left a guild in the past
        Args:
            user_id: The Discord ID of the user whose record to find
            guild_id: The Discord ID of the guild the user left
        Returns: A Row object containing data on the left member"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM left_members WHERE user_id=? AND guild_id=?"
        cursor.execute(sql, (user_id, guild_id))
        member = cursor.fetchone()
        self.db_connection.close_connection(connection)
        return member

    def get_left_member(self, user_id: int):
        """Find a specific user's leave records regardless of guild
        Args:
            user_id: The Discord ID of the member whose records to find
        Returns: A list of Row objects containing data on the selected user"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "SELECT * FROM left_members WHERE user_id=? ORDER BY leave_date ASC"
        cursor.execute(sql, (user_id,))
        members = cursor.fetchall()
        self.db_connection.close_connection(connection)
        return members

    def add_left_member(self, user_id: int, guild_id: int):
        """Mark a member as having left the guild
        Args:
            user_id: The Discord ID of the member who has left
            guild_id: The Discord ID of the guild the member has left"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "INSERT INTO left_members (user_id, guild_id, leave_date) VALUES (?, ?, datetime())"
        cursor.execute(sql, (user_id, guild_id))
        self.db_connection.commit_and_close(connection)

    def remove_left_member(self, user_id: int, guild_id: int):
        """Remove the record of a left member
        Args:
            user_id: The Discord ID of the member whose record to remove
            guild_id: The Discord ID of the guild from which to remove the record"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM left_members WHERE user_id=? AND guild_id=?"
        cursor.execute(sql, (user_id, guild_id))
        self.db_connection.commit_and_close(connection)

    def remove_all_member_records(self, user_id: int):
        """Remove all records of a left member regardless of guild
        Args:
            user_id: The Discord ID of the user whose records to remove"""

        connection, cursor = self.db_connection.connect_to_db()
        sql = "DELETE FROM left_members WHERE user_id=?"
        cursor.execute(sql, (user_id,))
        self.db_connection.commit_and_close(connection)
