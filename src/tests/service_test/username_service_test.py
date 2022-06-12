import unittest
import os
from services.username_service import UsernameService

class TestUsernameService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.username_service = UsernameService(db_address)

    def tearDown(self):
        self.username_service.clear_usernames()

    def test_usernames_are_found_correctly(self):
        self.username_service.add_username("Test", 1234)
        usernames = self.username_service.find_username("Test")
        self.assertEqual(usernames[0].username, "Test")

    def test_user_usernames_are_found_correctly(self):
        self.username_service.add_username("Test1", 1234)
        self.username_service.add_username("Test2", 2345)
        usernames = self.username_service.find_user_usernames(1234)
        self.assertEqual(len(usernames), 1)
        self.assertEqual(usernames[0].username, "Test1")

    def test_usernames_are_removed_correctly(self):
        self.username_service.add_username("Test", 1234)
        usernames = self.username_service.find_username("Test")
        self.assertEqual(len(usernames), 1)
        self.username_service.delete_username(usernames[0].db_id)
        usernames = self.username_service.find_username("Test")
        self.assertEqual(len(usernames), 0)

    def test_user_usernames_are_deleted_correctly(self):
        self.username_service.add_username("Test", 1234)
        self.username_service.add_username("Test", 2345)
        usernames = self.username_service.find_username("Test")
        self.assertEqual(len(usernames), 2)
        self.username_service.delete_user_usernames(1234)
        usernames = self.username_service.find_username("Test")
        self.assertEqual(len(usernames), 1)
        self.assertEqual(usernames[0].user_id, 2345)
