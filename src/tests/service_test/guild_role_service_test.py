import unittest
import os
from services.guild_role_service import GuildRoleService
from services.guild_role_category_service import GuildRoleCategoryService

class TestGuildRoleService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.guild_role_service = GuildRoleService(db_address)
        self.guild_role_category_service = GuildRoleCategoryService(db_address)
        self.guild_role_category_service.add_guild_role_category(1234, "Test1")
        self.guild_role_category_service.add_guild_role_category(1234, "Test2")
        self.guild_role_category_service.add_guild_role_category(2345, "Test1")
        self.category_test1 = self.guild_role_category_service.get_all_guild_role_categories(1234)[0]
        self.category_test2 = self.guild_role_category_service.get_all_guild_role_categories(1234)[1]
        self.category_test3 = self.guild_role_category_service.get_all_guild_role_categories(2345)[0]

    def tearDown(self):
        self.guild_role_service.clear_guild_roles()
        self.guild_role_category_service.clear_guild_role_categories()

    def test_guild_roles_are_found_correctly(self):
        self.guild_role_service.add_guild_role(9876, self.category_test1.db_id)
        roles = self.guild_role_service.get_all_guild_roles(1234)
        self.assertEqual(roles[0].role_id, 9876)

    def test_guild_roles_of_type_are_found_correctly(self):
        self.guild_role_service.add_guild_role(9876, self.category_test1.db_id)
        self.guild_role_service.add_guild_role(8765, self.category_test2.db_id)
        roles = self.guild_role_service.get_guild_roles_of_type("Test1", 1234)
        self.assertEqual(roles[0].role_id, 9876)

    def test_guild_roles_are_found_by_role_id(self):
        self.guild_role_service.add_guild_role(9876, self.category_test1.db_id)
        roles = self.guild_role_service.get_guild_roles_by_role_id(9876)
        self.assertEqual(len(roles), 1)

    def test_guild_roles_are_removed_from_a_category_correctly(self):
        self.guild_role_service.add_guild_role(9876, self.category_test1.db_id)
        self.guild_role_service.add_guild_role(9876, self.category_test2.db_id)
        roles = self.guild_role_service.get_guild_roles_by_role_id(9876)
        self.assertEqual(len(roles), 2)
        self.guild_role_service.remove_guild_role_from_category(9876, self.category_test1.db_id)
        roles = self.guild_role_service.get_guild_roles_by_role_id(9876)
        self.assertEqual(len(roles), 1)
        self.assertEqual(roles[0].category, "Test2")

    def test_all_guild_roles_are_removed_correctly(self):
        self.guild_role_service.add_guild_role(9876, self.category_test1.db_id)
        self.guild_role_service.add_guild_role(8765, self.category_test3.db_id)
        roles1 = self.guild_role_service.get_all_guild_roles(1234)
        roles2 = self.guild_role_service.get_all_guild_roles(2345)
        self.assertEqual(len(roles1), 1)
        self.assertEqual(len(roles2), 1)
        self.guild_role_service.delete_guild_roles(1234)
        roles1 = self.guild_role_service.get_all_guild_roles(1234)
        roles2 = self.guild_role_service.get_all_guild_roles(2345)
        self.assertEqual(len(roles1), 0)
        self.assertEqual(len(roles2), 1)
