import unittest
import os
from dao.reminders_dao import RemindersDAO
from datetime import datetime, timedelta

class TestRemindersDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.reminders_dao = RemindersDAO(self.db_addr)
        self.date1 = datetime.utcnow() + timedelta(days=1)
        self.date2 = datetime.utcnow() + timedelta(days=2)
        self.date3 = datetime.utcnow() + timedelta(days=3)
        self.expired1 = datetime.utcnow() + timedelta(days=-1)
        self.expired2 = datetime.utcnow() + timedelta(days=-2)

    def tearDown(self):
        self.reminders_dao.clear_reminders_table()

    def test_users_reminders_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date3)
        self.reminders_dao.add_new_reminder(2345, 8765, "Test2", self.date2)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test3", self.date1)
        rows = self.reminders_dao.get_reminders_by_user(1234)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["content"], "Test3")
        self.assertEqual(rows[1]["content"], "Test1")

    def test_users_public_reminders_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test2", self.date2, is_public=True)
        rows = self.reminders_dao.get_public_reminders_by_user(1234)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["content"], "Test2")

    def test_reminders_by_user_in_a_guild_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test2", self.date2)
        rows = self.reminders_dao.get_reminders_by_user_in_guild(1234, 9876)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["content"], "Test1")

    def test_public_reminders_by_user_in_a_guild_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test2", self.date2)
        self.reminders_dao.add_new_reminder(1234, 9876, "Test3", self.date3, is_public=True)
        rows = self.reminders_dao.get_public_reminders_by_user_in_guild(1234, 9876)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["content"], "Test3")

    def test_all_reminders_in_a_guild_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(2345, 9876, "Test2", self.date2)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test3", self.date3)
        rows = self.reminders_dao.get_reminders_in_guild(9876)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["content"], "Test1")
        self.assertEqual(rows[1]["content"], "Test2")

    def test_all_public_reminders_in_a_guild_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(2345, 8765, "Test2", self.date2)
        self.reminders_dao.add_new_reminder(3456, 9876, "Test3", self.date3, is_public=True)
        rows = self.reminders_dao.get_public_reminders_in_guild(9876)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["content"], "Test3")

    def test_public_reminders_created_outside_of_a_guild_cannot_be_found(self):
        self.reminders_dao.add_new_reminder(1234, None, "Test1", self.date1, is_public=True)
        self.reminders_dao.add_new_reminder(2345, None, "Test2", self.date2, is_public=True)
        rows = self.reminders_dao.get_public_reminders_in_guild(None)
        self.assertEqual(len(rows), 0)

    def test_expired_reminders_are_found_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(2345, 8765, "Test2", self.expired1)
        self.reminders_dao.add_new_reminder(3456, 7654, "Test3", self.expired2)
        rows = self.reminders_dao.get_expired_reminders()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["content"], "Test3")
        self.assertEqual(rows[1]["content"], "Test2")

    def test_reminder_is_found_correctly_by_id(self):
        db_id = self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)["id"]
        row = self.reminders_dao.get_reminder_by_id(db_id)
        self.assertEqual(row["content"], "Test1")

    def test_reminder_is_edited_correctly(self):
        db_id = self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)["id"]
        self.reminders_dao.edit_reminder(db_id, "Test2", self.date2, True, 120, 2)
        row = self.reminders_dao.get_reminder_by_id(db_id)
        self.assertEqual(row["content"], "Test2")
        self.assertEqual(row["reminder_date"], self.date2.strftime("%Y-%m-%d %H:%M:%S.%f"))
        self.assertTrue(row["public"])
        self.assertEqual(row["interval"], 120)
        self.assertEqual(row["repeats_left"], 2)

    def test_reminder_repeats_are_updated_correctly(self):
        db_id = self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.expired1, repeats=2)["id"]
        self.reminders_dao.update_reminder_repeats(db_id)
        row = self.reminders_dao.get_reminder_by_id(db_id)
        self.assertEqual(row["repeats_left"], 1)

    def test_reminder_repeats_are_not_updated_if_repeats_reaches_zero(self):
        db_id = self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.expired1)["id"]
        self.reminders_dao.update_reminder_repeats(db_id)
        self.reminders_dao.update_reminder_repeats(db_id)
        row = self.reminders_dao.get_reminder_by_id(db_id)
        self.assertEqual(row["repeats_left"], 0)

    def test_user_reminders_are_deleted_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test2", self.date2)
        self.reminders_dao.delete_user_reminders(1234)
        rows1 = self.reminders_dao.get_reminders_in_guild(9876)
        rows2 = self.reminders_dao.get_reminders_in_guild(8765)
        self.assertEqual(len(rows1), 0)
        self.assertEqual(len(rows2), 0)

    def test_user_reminders_in_a_guild_are_deleted_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(2345, 9876, "Test2", self.date2)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test3", self.date3)
        self.reminders_dao.delete_user_reminders_in_guild(1234, 9876)
        rows1 = self.reminders_dao.get_reminders_in_guild(9876)
        rows2 = self.reminders_dao.get_reminders_in_guild(8765)
        self.assertEqual(len(rows1), 1)
        self.assertEqual(rows1[0]["content"], "Test2")
        self.assertEqual(len(rows2), 1)
        self.assertEqual(rows2[0]["content"], "Test3")

    def test_guild_reminders_are_deleted_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)
        self.reminders_dao.add_new_reminder(2345, 8765, "Test2", self.date2)
        self.reminders_dao.add_new_reminder(3456, 9876, "Test3", self.date3)
        self.reminders_dao.delete_guild_reminders(9876)
        rows1 = self.reminders_dao.get_reminders_in_guild(9876)
        rows2 = self.reminders_dao.get_reminders_in_guild(8765)
        self.assertEqual(len(rows1), 0)
        self.assertEqual(len(rows2), 1)

    def test_reminders_are_deleted_correctly_by_id(self):
        db_id = self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1)["id"]
        self.reminders_dao.delete_reminder_by_id(db_id)
        row = self.reminders_dao.get_reminder_by_id(db_id)
        self.assertIsNone(row)

    def test_reminders_with_zero_repeats_are_deleted_correctly(self):
        self.reminders_dao.add_new_reminder(1234, 9876, "Test1", self.date1, repeats=-1)
        self.reminders_dao.add_new_reminder(1234, 8765, "Test2", self.date2, repeats=0)
        self.reminders_dao.add_new_reminder(1234, 7654, "Test3", self.date3, repeats=1)
        self.reminders_dao.delete_reminders_with_no_repeats()
        rows = self.reminders_dao.get_reminders_by_user(1234)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["content"], "Test1")
        self.assertEqual(rows[1]["content"], "Test3")
