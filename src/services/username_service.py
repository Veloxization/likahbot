"""The username service is used to call methods in the usernames DAO class. It'll be easier to
transfer to another database format as you will only have to edit the DAO classes while leaving
this class mostly intact."""

from dao.usernames_dao import UsernamesDAO
from entities.username_entity import UsernameEntity

class UsernameService:
    """A service for calling methods from usernames DAO
    Attributes:
        usernames_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for usernames DAO
        Args:
            db_address: The address for the database file where the usernames table resides"""

        self.usernames_dao = UsernamesDAO(db_address)

    def convert_to_entity(self, row):
        """Convert a database row to a username entity
        Args:
            row: The database row to convert to a username entity
        Returns: A username entity equivalent to the database row"""

        return UsernameEntity(row["id"], row["user_id"], row["username"], row["time"])

    def find_username(self, username: str):
        """Find the instances of a given username
        Args:
            username: The username to find
        Returns: A list of username entities"""

        rows = self.usernames_dao.find_username(username)
        return [self.convert_to_entity(row) for row in rows]

    def find_user_usernames(self, user_id: int):
        """Find all usernames for a given user
        Args:
            user_id: The Discord ID of the user whose previous usernames to find
        Returns: A list of username entities"""

        rows = self.usernames_dao.find_user_usernames(user_id)
        return [self.convert_to_entity(row) for row in rows]

    def add_username(self, username: str, user_id: int, username_limit: int = 5):
        """Add a new username. If more than limit names exist already, the oldest are deleted.
        Args:
            username: The username to add
            user_id: The Discord ID of the user this username is associated with
            username_limit: How many usernames for one user are allowed to be saved at a time"""

        self.usernames_dao.add_username(username, user_id, username_limit)

    def delete_username(self, username_id: int):
        """Delete a username record
        Args:
            username_id: The database ID for the username to delete"""

        self.usernames_dao.delete_username(username_id)

    def delete_user_usernames(self, user_id: int):
        """Delete all username records associated with a specific user
        Args:
            user_id: The Discord ID for the user whose username history to delete"""

        self.usernames_dao.delete_user_usernames(user_id)

    def clear_usernames_table(self):
        """Delete every single username record"""

        self.usernames_dao.clear_usernames_table()
