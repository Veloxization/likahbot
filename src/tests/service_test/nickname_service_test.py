import unittest
import os
from services.nickname_service import NicknameService

class TestNicknameService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.nickname_service = NicknameService(db_address)

    def tearDown(self):
        self.nickname_service.clear_nicknames()

    def test_nicknames_are_found_correctly(self):
        self.nickname_service.add_nickname("Test", 1234, 9876)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(nicknames[0].nickname, "Test")

    def test_user_nicknames_are_found_correctly(self):
        self.nickname_service.add_nickname("Test1", 1234, 9876)
        self.nickname_service.add_nickname("Test2", 2345, 9876)
        nicknames = self.nickname_service.find_user_nicknames(1234, 9876)
        self.assertEqual(len(nicknames), 1)
        self.assertEqual(nicknames[0].nickname, "Test1")

    def test_nicknames_are_removed_correctly(self):
        self.nickname_service.add_nickname("Test", 1234, 9876)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(len(nicknames), 1)
        self.nickname_service.delete_nickname(nicknames[0].db_id)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(len(nicknames), 0)

    def test_user_nicknames_are_removed_correctly(self):
        self.nickname_service.add_nickname("Test", 1234, 9876)
        self.nickname_service.add_nickname("Test", 2345, 9876)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(len(nicknames), 2)
        self.nickname_service.delete_user_nicknames(1234, 9876)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(len(nicknames), 1)
        self.assertEqual(nicknames[0].user_id, 2345)

    def test_guild_nicknames_are_removed_correctly(self):
        self.nickname_service.add_nickname("Test", 1234, 9876)
        self.nickname_service.add_nickname("Test", 1234, 8765)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(len(nicknames), 2)
        self.nickname_service.delete_guild_nicknames(9876)
        nicknames = self.nickname_service.find_nickname("Test")
        self.assertEqual(len(nicknames), 1)
        self.assertEqual(nicknames[0].guild_id, 8765)
