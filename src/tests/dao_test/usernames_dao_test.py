import asyncio
import unittest
import os
from dao.usernames_dao import UsernamesDAO

class TestUsernamesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.usernames_dao = UsernamesDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.usernames_dao.clear_usernames_table())

    def test_all_instances_of_username_are_found(self):
        asyncio.run(self.usernames_dao.add_username("Test", 1234))
        asyncio.run(self.usernames_dao.add_username("Test", 2345))
        asyncio.run(self.usernames_dao.add_username("Test2", 1234))
        usernames = asyncio.run(self.usernames_dao.find_username("Test"))
        self.assertEqual(len(usernames), 2)

    def test_all_instances_of_users_usernames_are_found(self):
        asyncio.run(self.usernames_dao.add_username("Test", 1234))
        asyncio.run(self.usernames_dao.add_username("Test", 2345))
        asyncio.run(self.usernames_dao.add_username("Test2", 1234))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 2)

    def test_username_is_added_correctly(self):
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 0)
        asyncio.run(self.usernames_dao.add_username("Test", 1234))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(usernames[0]["username"], "Test")

    def test_added_usernames_do_not_exceed_set_limit(self):
        asyncio.run(self.usernames_dao.add_username("Test1", 1234))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 1)
        asyncio.run(self.usernames_dao.add_username("Test2", 1234))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 2)
        asyncio.run(self.usernames_dao.add_username("Test3", 1234, 1))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 1)
        self.assertEqual(usernames[0]["username"], "Test3")

    def test_user_usernames_are_cleared_correctly(self):
        asyncio.run(self.usernames_dao.add_username("Test1", 1234))
        asyncio.run(self.usernames_dao.add_username("Test2", 1234))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 2)
        asyncio.run(self.usernames_dao.delete_user_usernames(1234))
        usernames = asyncio.run(self.usernames_dao.find_user_usernames(1234))
        self.assertEqual(len(usernames), 0)
