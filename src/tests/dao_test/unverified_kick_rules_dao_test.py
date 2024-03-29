import asyncio
import unittest
import os
from dao.unverified_kick_rules_dao import UnverifiedKickRulesDAO

class TestUnverifiedKickRulesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.unverified_kick_rules_dao = UnverifiedKickRulesDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.unverified_kick_rules_dao.clear_unverified_kick_rules_table())

    def test_guild_unverified_kick_rules_are_added_correctly(self):
        kick_rules = asyncio.run(self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(1234))
        self.assertIsNone(kick_rules)
        asyncio.run(self.unverified_kick_rules_dao.add_guild_unverified_kick_rules(1234, 60))
        kick_rules = asyncio.run(self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(1234))
        self.assertIsNotNone(kick_rules)

    def test_guild_unverified_kick_rules_are_edited_correctly(self):
        asyncio.run(self.unverified_kick_rules_dao.add_guild_unverified_kick_rules(1234, 60))
        kick_rules = asyncio.run(self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(1234))
        self.assertEqual(kick_rules["timedelta"], 60)
        asyncio.run(self.unverified_kick_rules_dao.edit_guild_unverified_kick_rules(1234, 120))
        kick_rules = asyncio.run(self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(1234))
        self.assertEqual(kick_rules["timedelta"], 120)

    def test_guild_unverified_kick_rules_are_removed_correctly(self):
        asyncio.run(self.unverified_kick_rules_dao.add_guild_unverified_kick_rules(1234, 60))
        kick_rules = asyncio.run(self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(1234))
        self.assertIsNotNone(kick_rules)
        asyncio.run(self.unverified_kick_rules_dao.remove_guild_unverified_kick_rules(1234))
        kick_rules = asyncio.run(self.unverified_kick_rules_dao.get_guild_unverified_kick_rules(1234))
        self.assertIsNone(kick_rules)
