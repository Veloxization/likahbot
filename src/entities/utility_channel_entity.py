"""Utility channel database rows converted into Python objects"""

class UtilityChannelEntity():
    """An object derived from the utility channels database table's rows
    Attributes:
        db_id: The database ID of the utility channel
        channel_id: The Discord ID of the channel
        guild_id: The Discord ID of the guild where the channel is
        channel_purpose: The purpose of this channel, e.g. LOG, RULES"""

    def __init__(self, db_id: int, channel_id: int, guild_id: int, channel_purpose: str):
        """Create a new utility channel entity
        Args:
            db_id: The database ID of the utility channel
            channel_id: The Discord ID of the channel
            guild_id: The Discord ID of the guild where the channel is
            channel_purpose: The purpose of this channel"""

        self.db_id = db_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.channel_purpose = channel_purpose
