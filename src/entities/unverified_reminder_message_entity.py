"""Unverified reminder message database rows converted into Python objects"""

class UnverifiedReminderMessageEntity():
    """An object derived from the unverified reminder messages database table's rows
    Attributes:
        db_id: The database ID of the unverified reminder message
        guild_id: The Discord ID of the guild this reminder message is associated with
        message: The verification reminder message that will be sent to an unverified user
        timedelta: The time in seconds until the message is sent, counted from time of joining"""

    def __init__(self, db_id: int, guild_id: int, message: str, timedelta: int):
        """Create a new unverified reminder message entity
        Args:
            db_id: The database ID of the unverified reminder message
            guild_id: The Discord ID of the guild this reminder message is associated with
            message: The verification reminder message that will be sent to an unverified user
            timedelta: The time in seconds until the message is sent, counted from time of
                       joining"""

        self.db_id = db_id
        self.guild_id = guild_id
        self.message = message
        self.timedelta = timedelta