import asyncio
import unittest
import os
from services.guild_role_category_service import GuildRoleCategoryService

class TestGuildRoleCategoryService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.guild_role_category_service = GuildRoleCategoryService(db_address)

    def tearDown(self):
        asyncio.run(self.guild_role_category_service.clear_guild_role_categories())

    def test_guild_role_categories_are_found_correctly(self):
        asyncio.run(self.guild_role_category_service.add_guild_role_category(1234, "TEST"))
        categories = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(1234))
        self.assertEqual(categories[0].category, "TEST")

    def test_guild_role_categories_are_removed_correctly(self):
        asyncio.run(self.guild_role_category_service.add_guild_role_category(1234, "TEST"))
        categories = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(1234))
        self.assertEqual(len(categories), 1)
        asyncio.run(self.guild_role_category_service.remove_guild_role_category(categories[0].db_id))
        categories = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(1234))
        self.assertEqual(len(categories), 0)

    def test_all_guild_role_categories_are_removed_correctly(self):
        asyncio.run(self.guild_role_category_service.add_guild_role_category(1234, "TEST"))
        asyncio.run(self.guild_role_category_service.add_guild_role_category(2345, "TEST"))
        categories1 = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(1234))
        categories2 = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(2345))
        self.assertEqual(len(categories1), 1)
        self.assertEqual(len(categories2), 1)
        asyncio.run(self.guild_role_category_service.remove_all_guild_role_categories(1234))
        categories1 = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(1234))
        categories2 = asyncio.run(self.guild_role_category_service.get_all_guild_role_categories(2345))
        self.assertEqual(len(categories1), 0)
        self.assertEqual(len(categories2), 1)
