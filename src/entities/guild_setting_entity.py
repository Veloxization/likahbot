"""Guild settings database rows converted into Python objects"""
from entities.master_entity import MasterEntity
from entities.setting_entity import SettingEntity

class GuildSettingEntity(MasterEntity):
    """An object derived from the guild settings database table's rows
    Attributes:
        db_id: The database ID of the setting
        guild_id: The Discord ID of the guild this setting is associated with
        setting: The default setting this setting is linked to
        value: The value of the setting"""

    def __init__(self, db_id: int, guild_id: int, setting: SettingEntity, value: str):
        """Create a new Guild Setting entity
        Args:
            db_id: The database ID of the setting
            guild_id: The Discord ID of the guild this setting is associated with
            setting: The default setting this setting is linked to
            value: The value of the setting"""

        self.db_id = db_id
        self.guild_id = guild_id
        self.setting = setting
        self.value = value
