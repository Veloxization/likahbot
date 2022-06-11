"""The left member service is used to call methods in the left members DAO class."""

from dao.left_members_dao import LeftMembersDAO
from entities.left_member_entity import LeftMemberEntity

class LeftMemberService:
    """A service for calling methods from left members DAO
    Attributes:
        left_members_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for left members DAO
        Args:
            db_address: The address for the database file where the left_members table resides"""

        self.left_members_dao = LeftMembersDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to a left member entity
        Args:
            row: The database row to convert to a left member entity
        Returns: A left member entity equivalent to the database row"""

        return LeftMemberEntity(row["id"], row["user_id"], row["guild_id"], row["leave_date"])

    def get_all_guild_left_members(self, guild_id: int):
        """Find all members who have left the specified guild
        Args:
            guild_id: The Discord ID of the guild whose left members to get
        Returns: A list of left member entities"""

        rows = self.left_members_dao.get_all_guild_left_members(guild_id)
        return [self._convert_to_entity(row) for row in rows]

    def get_all_left_members(self):
        """Find all members who have left any guild the bot is in
        Returns: A list of left member entities"""

        rows = self.left_members_dao.get_all_left_members()
        return [self._convert_to_entity(row) for row in rows]

    def get_guild_left_member(self, user_id: int, guild_id: int):
        """Find a specific member who has left a guild in the past
        Args:
            user_id: The Discord ID of the user whose record to find
            guild_id: The Discord ID of the guild the user left
        Returns: A left member entity"""

        row = self.left_members_dao.get_guild_left_member(user_id, guild_id)
        return self._convert_to_entity(row)

    def get_left_member(self, user_id: int):
        """Find a specific user's leave records regardless of guild
        Args:
            user_id: The Discord ID of the member whose records to find
        Returns: A list of left member entities"""

        rows = self.left_members_dao.get_left_member(user_id)
        return [self._convert_to_entity(row) for row in rows]

    def add_left_member(self, user_id: int, guild_id: int):
        """Mark a member as having left the guild
        Args:
            user_id: The Discord ID of the member who has left
            guild_id: The Discord ID of the guild the member has left"""

        self.left_members_dao.add_left_member(user_id, guild_id)

    def remove_left_member(self, user_id: int, guild_id: int):
        """Remove the record of a left member
        Args:
            user_id: The Discord ID of the member whose record to remove
            guild_id: The Discord ID of the guild from which to remove the record"""

        self.left_members_dao.remove_left_member(user_id, guild_id)

    def remove_all_member_records(self, user_id: int):
        """Remove all records of a left member regardless of guild
        Args:
            user_id: The Discord ID of the user whose records to remove"""

        self.left_members_dao.remove_all_member_records(user_id)

    def remove_guild_left_member_records(self, guild_id: int):
        """Remove all records of left members of a guild
        Args:
            guild_id: The Discord ID of the guild whose records to remove"""

        self.left_members_dao.remove_guild_left_member_records(guild_id)

    def clear_left_members(self):
        """Delete every single left member record"""

        self.left_members_dao.clear_left_members_table()
