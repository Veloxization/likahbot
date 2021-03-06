import unittest
import os
from dao.guild_role_categories_dao import GuildRoleCategoriesDAO

class TestGuildRoleCategoriesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.guild_role_categories_dao = GuildRoleCategoriesDAO(self.db_addr)

    def tearDown(self):
        self.guild_role_categories_dao.clear_guild_role_categories_table()

    def test_guild_role_categories_are_added_correctly(self):
        categories = self.guild_role_categories_dao.get_all_guild_role_categories(1234)
        self.assertEqual(len(categories), 0)
        self.guild_role_categories_dao.add_guild_role_category(1234, "TEST")
        categories = self.guild_role_categories_dao.get_all_guild_role_categories(1234)
        self.assertEqual(len(categories), 1)

    def test_guild_role_categories_are_removed_correctly(self):
        self.guild_role_categories_dao.add_guild_role_category(1234, "TEST")
        categories = self.guild_role_categories_dao.get_all_guild_role_categories(1234)
        self.assertEqual(len(categories), 1)
        self.guild_role_categories_dao.remove_guild_role_category(categories[0]["id"])
        categories = self.guild_role_categories_dao.get_all_guild_role_categories(1234)
        self.assertEqual(len(categories), 0)

    def test_all_guild_role_categories_are_removed_correctly(self):
        self.guild_role_categories_dao.add_guild_role_category(1234, "TEST")
        categories1 = self.guild_role_categories_dao.get_all_guild_role_categories(1234)
        self.assertEqual(len(categories1), 1)
        self.guild_role_categories_dao.add_guild_role_category(2345, "TEST")
        categories2 = self.guild_role_categories_dao.get_all_guild_role_categories(2345)
        self.assertEqual(len(categories2), 1)
        self.guild_role_categories_dao.remove_all_guild_role_categories(1234)
        categories1 = self.guild_role_categories_dao.get_all_guild_role_categories(1234)
        self.assertEqual(len(categories1), 0)
        categories2 = self.guild_role_categories_dao.get_all_guild_role_categories(2345)
        self.assertEqual(len(categories2), 1)
