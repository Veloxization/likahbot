import unittest
import os
from services.unverified_kick_rule_service import UnverifiedKickRuleService

class TestUnverifiedKickRuleService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.unverified_kick_rule_service = UnverifiedKickRuleService(db_address)

    def tearDown(self):
        self.unverified_kick_rule_service.clear_unverified_kick_rules()

    def test_guild_unverified_kick_rules_are_found_correctly(self):
        self.unverified_kick_rule_service.add_guild_unverified_kick_rules(1234, 300)
        rules = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(1234)
        self.assertEqual(rules.timedelta, 300)

    def test_guild_unverified_kick_rules_are_edited_correctly(self):
        self.unverified_kick_rule_service.add_guild_unverified_kick_rules(1234, 300)
        rules = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(1234)
        self.assertEqual(rules.timedelta, 300)
        self.unverified_kick_rule_service.edit_guild_unverified_kick_rules(1234, 600)
        rules = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(1234)
        self.assertEqual(rules.timedelta, 600)

    def test_guild_unverified_kick_rules_are_removed_correctly(self):
        self.unverified_kick_rule_service.add_guild_unverified_kick_rules(1234, 300)
        self.unverified_kick_rule_service.add_guild_unverified_kick_rules(2345, 600)
        rules1 = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(1234)
        rules2 = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(2345)
        self.assertIsNotNone(rules1)
        self.assertIsNotNone(rules2)
        self.unverified_kick_rule_service.remove_guild_unverified_kick_rules(1234)
        rules1 = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(1234)
        rules2 = self.unverified_kick_rule_service.get_guild_unverified_kick_rules(2345)
        self.assertIsNone(rules1)
        self.assertIsNotNone(rules2)
