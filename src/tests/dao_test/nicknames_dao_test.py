import asyncio
import unittest
import os
from dao.nicknames_dao import NicknamesDAO

class TestNicknamesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.nicknames_dao = NicknamesDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.nicknames_dao.clear_nicknames_table())

    def test_all_instances_of_nickname_are_found(self):
        asyncio.run(self.nicknames_dao.add_nickname("Test", 1234, 9876))
        asyncio.run(self.nicknames_dao.add_nickname("Test", 2345, 9876))
        asyncio.run(self.nicknames_dao.add_nickname("Test2", 1234, 9876))
        nicknames = asyncio.run(self.nicknames_dao.find_nickname("Test"))
        self.assertEqual(len(nicknames), 2)

    def test_all_instances_of_users_nicknames_are_found(self):
        asyncio.run(self.nicknames_dao.add_nickname("Test", 1234, 9876))
        asyncio.run(self.nicknames_dao.add_nickname("Test", 2345, 9876))
        asyncio.run(self.nicknames_dao.add_nickname("Test2", 1234, 9876))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 2)

    def test_nickname_is_added_correctly(self):
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 0)
        asyncio.run(self.nicknames_dao.add_nickname("Test", 1234, 9876))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(nicknames[0]["nickname"], "Test")

    def test_added_nicknames_do_not_exceed_set_limit(self):
        asyncio.run(self.nicknames_dao.add_nickname("Test1", 1234, 9876))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 1)
        asyncio.run(self.nicknames_dao.add_nickname("Test2", 1234, 9876))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 2)
        asyncio.run(self.nicknames_dao.add_nickname("Test3", 1234, 9876, 1))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 1)
        self.assertEqual(nicknames[0]["nickname"], "Test3")

    def test_user_nicknames_are_cleared_correctly(self):
        asyncio.run(self.nicknames_dao.add_nickname("Test1", 1234, 9876))
        asyncio.run(self.nicknames_dao.add_nickname("Test2", 1234, 8765))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 1)
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 8765))
        self.assertEqual(len(nicknames), 1)
        asyncio.run(self.nicknames_dao.delete_user_nicknames(1234, 9876))
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 9876))
        self.assertEqual(len(nicknames), 0)
        nicknames = asyncio.run(self.nicknames_dao.find_user_nicknames(1234, 8765))
        self.assertEqual(len(nicknames), 1)
