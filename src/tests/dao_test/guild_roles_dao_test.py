import asyncio
import unittest
import os
from dao.guild_roles_dao import GuildRolesDAO
from dao.guild_role_categories_dao import GuildRoleCategoriesDAO

class TestGuildRolesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.guild_roles_dao = GuildRolesDAO(self.db_addr)
        self.guild_role_categories_dao = GuildRoleCategoriesDAO(self.db_addr)
        asyncio.run(self.guild_role_categories_dao.add_guild_role_category(1234, "TEST"))
        asyncio.run(self.guild_role_categories_dao.add_guild_role_category(2345, "TEST"))
        self.category_id1 = asyncio.run(self.guild_role_categories_dao.get_all_guild_role_categories(1234))[0]["id"]
        self.category_id2 = asyncio.run(self.guild_role_categories_dao.get_all_guild_role_categories(2345))[0]["id"]

    def tearDown(self):
        asyncio.run(self.guild_roles_dao.clear_guild_roles_table())
        asyncio.run(self.guild_role_categories_dao.clear_guild_role_categories_table())

    def test_guild_role_is_added_correctly(self):
        roles = asyncio.run(self.guild_roles_dao.get_all_guild_roles(1234))
        self.assertEqual(len(roles), 0)
        asyncio.run(self.guild_roles_dao.add_guild_role(9876, self.category_id1))
        roles = asyncio.run(self.guild_roles_dao.get_all_guild_roles(1234))
        self.assertEqual(len(roles), 1)

    def test_guild_role_is_removed_correctly(self):
        asyncio.run(self.guild_role_categories_dao.add_guild_role_category(1234, "TEST2"))
        cat_id = asyncio.run(self.guild_role_categories_dao.get_all_guild_role_categories(1234))[1]["id"]
        asyncio.run(self.guild_roles_dao.add_guild_role(9876, self.category_id1))
        asyncio.run(self.guild_roles_dao.add_guild_role(9876, cat_id))
        roles = asyncio.run(self.guild_roles_dao.get_all_guild_roles(1234))
        self.assertEqual(len(roles), 2)
        asyncio.run(self.guild_roles_dao.remove_guild_role_from_category(9876, self.category_id1))
        roles = asyncio.run(self.guild_roles_dao.get_all_guild_roles(1234))
        self.assertEqual(len(roles), 1)

    def test_all_guild_roles_are_removed_correctly(self):
        asyncio.run(self.guild_roles_dao.add_guild_role(9876, self.category_id1))
        asyncio.run(self.guild_roles_dao.add_guild_role(8765, self.category_id2))
        roles1 = asyncio.run(self.guild_roles_dao.get_all_guild_roles(1234))
        roles2 = asyncio.run(self.guild_roles_dao.get_all_guild_roles(2345))
        self.assertEqual(len(roles1), 1)
        self.assertEqual(len(roles2), 1)
        asyncio.run(self.guild_roles_dao.delete_guild_roles(1234))
        roles1 = asyncio.run(self.guild_roles_dao.get_all_guild_roles(1234))
        roles2 = asyncio.run(self.guild_roles_dao.get_all_guild_roles(2345))
        self.assertEqual(len(roles1), 0)
        self.assertEqual(len(roles2), 1)

    def test_guild_roles_of_type_are_returned_correctly(self):
        asyncio.run(self.guild_role_categories_dao.add_guild_role_category(1234, "TEST2"))
        cat_id = asyncio.run(self.guild_role_categories_dao.get_all_guild_role_categories(1234))[1]["id"]
        asyncio.run(self.guild_roles_dao.add_guild_role(9876, self.category_id1))
        asyncio.run(self.guild_roles_dao.add_guild_role(8765, self.category_id1))
        asyncio.run(self.guild_roles_dao.add_guild_role(7654, cat_id))
        roles = asyncio.run(self.guild_roles_dao.get_guild_roles_of_type("TEST", 1234))
        self.assertEqual(len(roles), 2)
        roles = asyncio.run(self.guild_roles_dao.get_guild_roles_of_type("TEST2", 1234))
        self.assertEqual(len(roles), 1)

    def test_guild_role_is_returned_correctly_with_id(self):
        asyncio.run(self.guild_roles_dao.add_guild_role(9876, self.category_id1))
        asyncio.run(self.guild_roles_dao.add_guild_role(8765, self.category_id2))
        role = asyncio.run(self.guild_roles_dao.get_guild_roles_by_role_id(9876))[0]
        self.assertEqual(role["role_id"], 9876)
        self.assertEqual(role["guild_id"], 1234)
        self.assertEqual(role["category"], "TEST")
