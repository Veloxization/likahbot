"""Unverified kick rule database rows converted into Python objects"""

from entities.master_entity import MasterEntity

class UnverifiedKickRuleEntity(MasterEntity):
    """An object derived from the unverified kick rules database table's rows
    Attributes:
        timedelta: The time in seconds until an unverified member is kicked"""

    def __init__(self, timedelta: int):
        """Create a new unverified kick rule entity
        Args:
            timedelta: The time in seconds until an unverified member is kicked"""

        self.timedelta = timedelta
