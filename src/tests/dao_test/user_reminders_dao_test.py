import asyncio
import unittest
import os
from dao.reminders_dao import RemindersDAO
from dao.user_reminders_dao import UserRemindersDAO
from datetime import datetime, timedelta

class TestUserRemindersDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.reminders_dao = RemindersDAO(self.db_addr)
        self.user_reminders_dao = UserRemindersDAO(self.db_addr)
        self.date1 = datetime.utcnow() + timedelta(days=1)
        self.date2 = datetime.utcnow() + timedelta(days=2)
        self.date3 = datetime.utcnow() + timedelta(days=3)
        self.reminder_id1 = asyncio.run(self.reminders_dao.add_new_reminder(1234, 9876, "test1", self.date1, "time"))["id"]
        self.reminder_id2 = asyncio.run(self.reminders_dao.add_new_reminder(2345, 8765, "test2", self.date2, "time"))["id"]
        self.reminder_id3 = asyncio.run(self.reminders_dao.add_new_reminder(1234, 8765, "test3", self.date3, "time"))["id"]

    def tearDown(self):
        asyncio.run(self.reminders_dao.clear_reminders_table())

    def test_users_reminders_are_found_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id1))
        rows = asyncio.run(self.user_reminders_dao.get_user_reminders(1234))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["reminder_id"], self.reminder_id1)
        self.assertEqual(rows[1]["reminder_id"], self.reminder_id2)

    def test_users_reminders_in_guild_are_found_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id3))
        rows = asyncio.run(self.user_reminders_dao.get_user_reminders_in_guild(1234, 8765))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["reminder_id"], self.reminder_id2)
        self.assertEqual(rows[1]["reminder_id"], self.reminder_id3)

    def test_user_reminders_of_reminder_id_are_found_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id2))
        rows = asyncio.run(self.user_reminders_dao.get_user_reminders_of_reminder_id(self.reminder_id1))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["reminder_id"], self.reminder_id1)
        self.assertEqual(rows[1]["reminder_id"], self.reminder_id1)

    def test_user_reminders_are_found_by_id(self):
        user_reminder_id = asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))["id"]
        row = asyncio.run(self.user_reminders_dao.get_user_reminder_by_id(user_reminder_id))
        self.assertEqual(row["reminder_id"], self.reminder_id1)

    def test_user_reminders_of_reminder_id_are_deleted_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.delete_user_reminders_of_reminder_id(self.reminder_id1))
        rows1 = asyncio.run(self.user_reminders_dao.get_user_reminders_of_reminder_id(self.reminder_id1))
        rows2 = asyncio.run(self.user_reminders_dao.get_user_reminders_of_reminder_id(self.reminder_id2))
        self.assertEqual(len(rows1), 0)
        self.assertEqual(len(rows2), 1)

    def test_users_user_reminders_are_deleted_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.delete_user_reminders_of_user(1234))
        rows1 = asyncio.run(self.user_reminders_dao.get_user_reminders(1234))
        rows2 = asyncio.run(self.user_reminders_dao.get_user_reminders(2345))
        self.assertEqual(len(rows1), 0)
        self.assertEqual(len(rows2), 1)

    def test_user_reminders_of_user_within_guild_are_deleted_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id3))
        asyncio.run(self.user_reminders_dao.delete_user_reminders_of_user_in_guild(1234, 8765))
        rows1 = asyncio.run(self.user_reminders_dao.get_user_reminders(1234))
        rows2 = asyncio.run(self.user_reminders_dao.get_user_reminders(2345))
        self.assertEqual(len(rows1), 1)
        self.assertEqual(len(rows2), 1)
        self.assertNotEqual(rows1[0]["creator_guild_id"], 8765)
        self.assertEqual(rows1[0]["reminder_id"], self.reminder_id1)
        self.assertEqual(rows2[0]["reminder_id"], self.reminder_id2)

    def test_user_reminder_is_deleted_correctly_by_id(self):
        user_reminder_id = asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))["id"]
        asyncio.run(self.user_reminders_dao.delete_user_reminder_by_id(user_reminder_id))
        row = asyncio.run(self.user_reminders_dao.get_user_reminder_by_id(user_reminder_id))
        self.assertIsNone(row)

    def test_user_reminder_table_is_cleared_correctly(self):
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.create_user_reminder(2345, self.reminder_id2))
        asyncio.run(self.user_reminders_dao.create_user_reminder(1234, self.reminder_id3))
        asyncio.run(self.user_reminders_dao.clear_user_reminders_table())
        rows1 = asyncio.run(self.user_reminders_dao.get_user_reminders(1234))
        rows2 = asyncio.run(self.user_reminders_dao.get_user_reminders(2345))
        self.assertEqual(len(rows1), 0)
        self.assertEqual(len(rows2), 0)
