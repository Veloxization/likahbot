import asyncio
import unittest
import os
from datetime import datetime, timedelta
from services.reminder_service import ReminderService

class TestReminderService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.reminder_service = ReminderService(db_address)
        self.date1 = datetime.utcnow() + timedelta(days=1)
        self.date2 = datetime.utcnow() + timedelta(days=2)
        self.date3 = datetime.utcnow() + timedelta(days=3)
        self.expired1 = datetime.utcnow() + timedelta(days=-1)
        self.expired2 = datetime.utcnow() + timedelta(days=-2)

    def tearDown(self):
        asyncio.run(self.reminder_service.clear_reminders())

    def test_reminders_by_user_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(2345, 8765, "test2", self.date2, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test3", self.date3, "time"))
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(1234))
        self.assertEqual(len(reminders), 2)
        self.assertEqual(reminders[0].content, "test1")
        self.assertEqual(reminders[1].content, "test3")

    def test_public_reminders_by_user_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test2", self.date1, "time", is_public=True))
        reminders = asyncio.run(self.reminder_service.get_public_reminders_by_user(1234))
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].content, "test2")

    def test_reminders_by_user_in_guild_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test2", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(2345, 8765, "test3", self.date1, "time"))
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user_in_guild(1234, 8765))
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].content, "test2")

    def test_public_reminders_by_user_in_guild_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test2", self.date2, "time", is_public=True))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test3", self.date3, "time", is_public=True))
        reminders = asyncio.run(self.reminder_service.get_public_reminders_by_user_in_guild(1234, 9876))
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].content, "test2")

    def test_reminders_in_guild_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(2345, 9876, "test2", self.date2, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(3456, 8765, "test3", self.date3, "time"))
        reminders = asyncio.run(self.reminder_service.get_reminders_in_guild(9876))
        self.assertEqual(len(reminders), 2)
        self.assertEqual(reminders[0].content, "test1")
        self.assertEqual(reminders[1].content, "test2")

    def test_public_reminders_in_guild_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(2345, 9876, "test2", self.date2, "time", is_public=True))
        asyncio.run(self.reminder_service.add_new_reminder(3456, 8765, "test3", self.date3, "time", is_public=True))
        reminders = asyncio.run(self.reminder_service.get_public_reminders_in_guild(9876))
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].content, "test2")

    def test_expired_reminders_are_found_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(2345, 9876, "test2", self.expired1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(3456, 8765, "test3", self.expired2, "time"))
        reminders = asyncio.run(self.reminder_service.get_expired_reminders())
        self.assertEqual(len(reminders), 2)
        self.assertEqual(reminders[0].content, "test3")
        self.assertEqual(reminders[1].content, "test2")

    def test_reminder_is_found_correctly_by_id(self):
        reminder_id = asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        reminder = asyncio.run(self.reminder_service.get_reminder_by_id(reminder_id))
        self.assertIsNotNone(reminder)

    def test_reminder_is_edited_correctly(self):
        reminder_id = asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.edit_reminder(reminder_id, "test2", self.date2, True, 60, "date", 3))
        reminder = asyncio.run(self.reminder_service.get_reminder_by_id(reminder_id))
        self.assertEqual(reminder.content, "test2")
        self.assertEqual(reminder.reminder_date, datetime.strftime(self.date2, "%Y-%m-%d %H:%M:%S.%f"))
        self.assertTrue(reminder.is_public)
        self.assertEqual(reminder.interval, 60)
        self.assertEqual(reminder.reminder_type, "date")
        self.assertEqual(reminder.repeats_left, 3)

    def test_reminder_repeats_are_updated_correctly(self):
        reminder_id = asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time", repeats=3))
        asyncio.run(self.reminder_service.update_reminder_repeats(reminder_id))
        reminder = asyncio.run(self.reminder_service.get_reminder_by_id(reminder_id))
        self.assertEqual(reminder.repeats_left, 2)

    def test_user_reminders_are_deleted_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(2345, 9876, "test2", self.date2, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test3", self.date3, "time"))
        asyncio.run(self.reminder_service.delete_user_reminders(1234))
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(1234))
        self.assertEqual(len(reminders), 0)
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(2345))
        self.assertEqual(len(reminders), 1)

    def test_user_reminders_in_guild_are_deleted_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test2", self.date2, "time"))
        asyncio.run(self.reminder_service.delete_user_reminders_in_guild(1234, 9876))
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(1234))
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].content, "test2")

    def test_reminders_in_guild_are_deleted_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test2", self.date2, "time"))
        asyncio.run(self.reminder_service.add_new_reminder(1234, 8765, "test3", self.date3, "time"))
        asyncio.run(self.reminder_service.delete_guild_reminders(9876))
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(1234))
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0].content, "test3")

    def test_reminders_are_deleted_correctly_by_id(self):
        reminder_id = asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time"))
        asyncio.run(self.reminder_service.delete_reminder_by_id(reminder_id))
        reminder = asyncio.run(self.reminder_service.get_reminder_by_id(reminder_id))
        self.assertIsNone(reminder)

    def test_reminders_with_no_repeats_are_deleted_correctly(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time", repeats=0))
        asyncio.run(self.reminder_service.delete_reminders_with_no_repeats())
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(1234))
        self.assertEqual(len(reminders), 0)

    def test_reminders_with_negative_repeats_are_not_inadvertently_deleted(self):
        asyncio.run(self.reminder_service.add_new_reminder(1234, 9876, "test1", self.date1, "time", repeats=-1))
        asyncio.run(self.reminder_service.delete_reminders_with_no_repeats())
        reminders = asyncio.run(self.reminder_service.get_reminders_by_user(1234))
        self.assertEqual(len(reminders), 1)
