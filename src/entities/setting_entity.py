"""Settings database rows converted into Python objects"""
from entities.master_entity import MasterEntity

class SettingEntity(MasterEntity):
    """An object derived from the settings database table's rows
    Attributes:
        db_id: The database ID of the setting
        name: The name of the setting
        value: The default value of the setting"""

    def __init__(self, db_id: int, name: str, value: str):
        """Create a new Setting entity
        Args:
            db_id: The database ID of the setting
            name: The name of the setting
            value: The default value of the setting"""

        self.db_id = db_id
        self.name = name
        self.value = value
