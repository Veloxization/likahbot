"""Unverified kick rule database rows converted into Python objects"""

class UnverifiedKickRuleEntity():
    """An object derived from the unverified kick rules database table's rows
    Attributes:
        db_id: The database ID of the unverified kick rule
        guild_id: The Discord ID of the guild the kick rule applies for
        timedelta: The time in seconds until an unverified member is kicked"""

    def __init__(self, db_id: int, guild_id: int, timedelta: int):
        """Create a new unverified kick rule entity
        Args:
            db_id: The database ID of the utility channel
            guild_id: The Discord ID of the guild the kick rule applies for
            timedelta: The time in seconds until an unverified member is kicked"""

        self.db_id = db_id
        self.guild_id = guild_id
        self.timedelta = timedelta
