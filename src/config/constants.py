"""Houses the constants enumerator"""
from enum import Enum

class Constants(Enum):
    """An enumerator class for constants for easy setup"""
    DB_ADDRESS = "database/likahbotdatabase.db"
    DEBUG_GUILDS = [383107941173166083] # set to [] for global slash commands
