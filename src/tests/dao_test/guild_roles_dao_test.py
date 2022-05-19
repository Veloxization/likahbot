import unittest
import os
from dao.guild_roles_dao import GuildRolesDAO

class TestGuildRolesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.guild_roles_dao = GuildRolesDAO(self.db_addr)

    def tearDown(self):
        self.guild_roles_dao.clear_guild_roles_table()

    def test_guild_role_is_added_correctly(self):
        roles = self.guild_roles_dao.get_all_guild_roles(2345)
        self.assertEqual(len(roles), 0)
        self.guild_roles_dao.add_guild_role(1234, 2345, "TEST")
        roles = self.guild_roles_dao.get_all_guild_roles(2345)
        self.assertEqual(len(roles), 1)

    def test_guild_role_is_removed_correctly(self):
        self.guild_roles_dao.add_guild_role(1234, 2345, "TEST")
        self.guild_roles_dao.add_guild_role(4321, 2345, "TEST")
        roles = self.guild_roles_dao.get_all_guild_roles(2345)
        self.assertEqual(len(roles), 2)
        self.guild_roles_dao.remove_guild_role(1234)
        roles = self.guild_roles_dao.get_all_guild_roles(2345)
        self.assertEqual(len(roles), 1)

    def test_all_guild_roles_are_removed_correctly(self):
        self.guild_roles_dao.add_guild_role(1234, 2345, "TEST")
        self.guild_roles_dao.add_guild_role(4321, 5432, "TEST")
        roles1 = self.guild_roles_dao.get_all_guild_roles(2345)
        roles2 = self.guild_roles_dao.get_all_guild_roles(5432)
        self.assertEqual(len(roles1), 1)
        self.assertEqual(len(roles2), 1)
        self.guild_roles_dao.delete_guild_roles(2345)
        roles1 = self.guild_roles_dao.get_all_guild_roles(2345)
        roles2 = self.guild_roles_dao.get_all_guild_roles(5432)
        self.assertEqual(len(roles1), 0)
        self.assertEqual(len(roles2), 1)

    def test_guild_roles_of_type_are_returned_correctly(self):
        self.guild_roles_dao.add_guild_role(1234, 2345, "TEST1")
        self.guild_roles_dao.add_guild_role(4321, 2345, "TEST1")
        self.guild_roles_dao.add_guild_role(3412, 2345, "TEST2")
        roles = self.guild_roles_dao.get_guild_roles_of_type("TEST1", 2345)
        self.assertEqual(len(roles), 2)
        roles = self.guild_roles_dao.get_guild_roles_of_type("TEST2", 2345)
        self.assertEqual(len(roles), 1)

    def test_guild_role_is_returned_correctly_with_id(self):
        self.guild_roles_dao.add_guild_role(1234, 2345, "TEST1")
        self.guild_roles_dao.add_guild_role(4321, 5432, "TEST2")
        role = self.guild_roles_dao.get_guild_role_by_role_id(4321)
        self.assertEqual(role["role_id"], 4321)
        self.assertEqual(role["guild_id"], 5432)
        self.assertEqual(role["type"], "TEST2")
