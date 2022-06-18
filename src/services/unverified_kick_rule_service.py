"""The unverified kick rule service is used to call methods in the unverified kick rules DAO
class."""

from dao.unverified_kick_rules_dao import UnverifiedKickRulesDAO
from entities.unverified_kick_rule_entity import UnverifiedKickRuleEntity

class UnverifiedKickRuleService:
    """A service for calling methods from unverified kick rules DAO
    Attributes:
        unverified_kick_rules_dao: The DAO object this service will use"""

    def __init__(self, db_address):
        """Create a new service for unverified kick rules DAO
        Args:
            db_address: The address for the database file where the unverified kick rules table
                        resides"""

        self.unverified_kick_rules_dao = UnverifiedKickRulesDAO(db_address)

    def _convert_to_entity(self, row):
        """Convert a database row to an unverified kick rule entity
        Args:
            row: The database row to convert to an unverified kick rule entity
        Returns: An unverified kick rule entity equivalent to the database row"""

        if not row:
            return None
        return UnverifiedKickRuleEntity(row["timedelta"])

    def get_guild_unverified_kick_rules(self, guild_id: int):
        """Get the rules for kicking unverified members from specified guild
        Args:
            guild_id: The Discord ID of the guild whose kick rules to get
        Returns: An unverified kick rule entity"""

        row = self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(guild_id)
        return self._convert_to_entity(row)

    def add_guild_unverified_kick_rules(self, guild_id: int, kick_timing: int):
        """Create a new unverified kick rule for a guild
        Args:
            guild_id: The Discord ID of the guild which will be getting this kick rule
            kick_timing: The time, in seconds, it takes before an unverified member is kicked,
                         counted from the time of joining the guild."""

        self.unverified_kick_rules_dao.add_guild_unverified_kick_rules(guild_id, kick_timing)

    def edit_guild_unverified_kick_rules(self, guild_id: int, kick_timing: int):
        """Edit the timing for a guild's unverified kick timing
        Args:
            guild_id: The Discord ID of the guild whose kick rules to edit
            kick_timing: The new time, in seconds, it takes before and unverified member is
                         kicked"""

        self.unverified_kick_rules_dao.edit_guild_unverified_kick_rules(guild_id, kick_timing)

    def remove_guild_unverified_kick_rules(self, guild_id: int):
        """Remove the kick rules of a specific guild
        Args:
            guild_id: The Discord ID of the guild whose kick rules to remove"""

        self.unverified_kick_rules_dao.remove_guild_unverified_kick_rules(guild_id)

    def clear_unverified_kick_rules(self):
        """Delete every single unverified kick rule"""

        self.unverified_kick_rules_dao.clear_unverified_kick_rules_table()
