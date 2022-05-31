"""Punishment database rows converted into Python objects"""

from time_handler.time import TimeStringConverter

class PunishmentEntity():
    """An object derived from the punishments database table's rows
    Attributes:
        db_id: The database ID of the punishment
        user_id: The Discord ID of the user that was punished
        issuer_id: The Discord ID of the moderator who issued the punishment
        guild_id: The Discord ID of the guild where this punishment was issued
        punishment_type: The type of punishment (e.g. WARN, KICK, BAN)
        reason: The given reason for the punishment
        time: A datetime object telling the time this punishment was issued
        deleted: A boolean telling whether this punishment has been deleted"""

    def __init__(self, db_id: int, user_id: int, issuer_id: int, guild_id: int,
                 punishment_type: str, time: str, reason: str = None, deleted: bool = False):
        """Create a new Punishment entity
        Args:
            db_id: The database ID of the punishment
            user_id: The Discord ID of the user that was punished
            issuer_id: The Discord ID of the moderator who issued the punishment
            guild_id: The Discord ID of the guild where this punishment was issued
            punishment_type: The type of punishment (e.g. WARN, KICK, BAN)
            time: A datetime object telling the time this punishment was issued
            reason: The given reason for the punishment
            deleted: A boolean telling whether this punishment has been deleted"""

        self.db_id = db_id
        self.user_id = user_id
        self.issuer_id = issuer_id
        self.guild_id = guild_id
        self.punishment_type = punishment_type
        self.reason = reason
        self.time = time
        self.deleted = deleted
