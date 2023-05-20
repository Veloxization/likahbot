import asyncio
import unittest
import os
from datetime import datetime, timedelta
from services.reminder_service import ReminderService
from services.user_reminder_service import UserReminderService

class TestUserReminderService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/test_schema.sql")
        self.user_reminder_service = UserReminderService(db_address)
        self.reminder_service = ReminderService(db_address)
        self.date1 = datetime.utcnow() + timedelta(days=1)
        self.date2 = datetime.utcnow() + timedelta(days=2)
        self.date3 = datetime.utcnow() + timedelta(days=3)
        self.reminder_id1 = asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        self.reminder_id2 = asyncio.run(self.reminder_service.add_new_reminder(2345, 8765, "test2", self.date2, "time"))
        self.reminder_id3 = asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test3", self.date3, "time"))

    def tearDown(self):
        asyncio.run(self.reminder_service.clear_reminders())

    def test_user_reminders_are_found_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminder_service.create_user_reminder(2345, self.reminder_id1))
        user_reminders = asyncio.run(self.user_reminder_service.get_user_reminders(1234))
        self.assertEqual(len(user_reminders), 1)
        self.assertEqual(user_reminders[0].user_id, 1234)

    def test_user_reminders_in_guild_are_found_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id2))
        user_reminders = asyncio.run(self.user_reminder_service.get_user_reminders_in_guild(1234, 9876))
        self.assertEqual(len(user_reminders), 1)
        self.assertEqual(user_reminders[0].reminder.guild_id, 9876)

    def test_user_reminders_of_reminder_id_are_found_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminder_service.create_user_reminder(2345, self.reminder_id2))
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id3))
        user_reminders = asyncio.run(self.user_reminder_service.get_user_reminders_of_reminder_id(self.reminder_id2))
        self.assertEqual(len(user_reminders), 2)
        self.assertNotEqual(user_reminders[0].reminder.db_id, self.reminder_id1)
        self.assertNotEqual(user_reminders[0].reminder.db_id, self.reminder_id3)
        self.assertNotEqual(user_reminders[1].reminder.db_id, self.reminder_id1)
        self.assertNotEqual(user_reminders[1].reminder.db_id, self.reminder_id3)

    def test_user_reminder_is_found_correctly_by_id(self):
        user_reminder_id = asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id1))
        user_reminder = asyncio.run(self.user_reminder_service.get_user_reminder_by_id(user_reminder_id))
        self.assertEqual(user_reminder.db_id, user_reminder_id)

    def test_user_reminders_of_reminder_id_are_deleted_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id3))
        asyncio.run(self.user_reminder_service.delete_user_reminders_of_reminder_id(self.reminder_id2))
        user_reminders = asyncio.run(self.user_reminder_service.get_user_reminders(1234))
        self.assertEqual(len(user_reminders), 1)
        self.assertNotEqual(user_reminders[0].reminder.db_id, self.reminder_id2)

    def test_users_reminders_are_deleted_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminder_service.create_user_reminder(2345, self.reminder_id2))
        asyncio.run(self.user_reminder_service.delete_user_reminders_of_user(1234))
        user_reminders = asyncio.run(self.user_reminder_service.get_user_reminders_of_reminder_id(self.reminder_id2))
        self.assertEqual(len(user_reminders), 1)
        self.assertNotEqual(user_reminders[0].user_id, 1234)

    def test_user_reminders_of_user_in_guild_are_deleted_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id2))
        asyncio.run(self.user_reminder_service.delete_user_reminders_of_user_in_guild(1234, 9876))
        user_reminders = asyncio.run(self.user_reminder_service.get_user_reminders(1234))
        self.assertEqual(len(user_reminders), 1)
        self.assertNotEqual(user_reminders[0].reminder.guild_id, 9876)

    def test_user_reminder_is_deleted_correctly_by_id(self):
        user_reminder_id = asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminder_service.delete_user_reminder_by_id(user_reminder_id))
        user_reminder = asyncio.run(self.user_reminder_service.get_user_reminder_by_id(user_reminder_id))
        self.assertIsNone(user_reminder)

    def test_all_user_reminders_are_deleted_correctly(self):
        asyncio.run(self.user_reminder_service.create_user_reminder(1234, self.reminder_id1))
        asyncio.run(self.user_reminder_service.create_user_reminder(2345, self.reminder_id2))
        asyncio.run(self.user_reminder_service.create_user_reminder(3456, self.reminder_id3))
        asyncio.run(self.user_reminder_service.clear_user_reminders())
        user_reminders1 = asyncio.run(self.user_reminder_service.get_user_reminders(1234))
        user_reminders2 = asyncio.run(self.user_reminder_service.get_user_reminders(2345))
        user_reminders3 = asyncio.run(self.user_reminder_service.get_user_reminders(3456))
        self.assertEqual(len(user_reminders1), 0)
        self.assertEqual(len(user_reminders2), 0)
        self.assertEqual(len(user_reminders3), 0)
