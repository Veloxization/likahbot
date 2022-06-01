"""Nickname database rows converted into Python objects"""

from time_handler.time import TimeStringConverter

class NicknameEntity():
    """An object derived from the nicknames database table's rows
    Attributes:
        db_id: The database ID of the nickname
        user_id: The Discord ID of the user this nickname is tied to
        nickname: The nickname string
        guild_id: The Discord ID of the guild this nickname is tied to
        time: A datetime object telling the time this nickname came to be used"""

    def __init__(self, db_id: int, user_id: int, nickname: str, guild_id: int, time: str):
        """Create a new Nickname entity
        Args:
            db_id: The database ID of the nickname
            user_id: The Discord ID of the user this nickname is tied to
            nickname: The nickname string
            guild_id: The Discord ID of the guild this nickname is tied to
            time: The time string telling the time this nickname came to be used"""

        self.db_id = db_id
        self.user_id = user_id
        self.nickname = nickname
        self.guild_id = guild_id
        converter = TimeStringConverter()
        self.time = converter.string_to_datetime(time)
