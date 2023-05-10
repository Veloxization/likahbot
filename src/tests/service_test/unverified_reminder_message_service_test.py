import asyncio
import unittest
import os
from services.unverified_reminder_message_service import UnverifiedReminderMessageService

class TestUnverifiedReminderMessageService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.unverified_reminder_message_service = UnverifiedReminderMessageService(db_address)

    def tearDown(self):
        asyncio.run(self.unverified_reminder_message_service.clear_unverified_reminder_messages())

    def test_all_unverified_reminder_messages_are_found_correctly(self):
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(1234, "Test1", 60))
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(2345, "Test2", 60))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(len(messages), 2)

    def test_guild_unverified_reminder_messages_are_found_correctly(self):
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(1234, "Test1", 60))
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(2345, "Test2", 60))
        messages = asyncio.run(self.unverified_reminder_message_service.get_guild_unverified_reminder_messages(1234))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Test1")

    def test_unverified_reminder_messages_are_edited_correctly(self):
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(1234, "Test1", 60))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(messages[0].message, "Test1")
        self.assertEqual(messages[0].timedelta, 60)
        asyncio.run(self.unverified_reminder_message_service.edit_guild_unverified_message(messages[0].db_id, "Test2", 120))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(messages[0].message, "Test2")
        self.assertEqual(messages[0].timedelta, 120)

    def test_unverified_reminder_messages_are_deleted_correctly(self):
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(1234, "Test", 60))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(len(messages), 1)
        asyncio.run(self.unverified_reminder_message_service.delete_unverified_reminder_message(messages[0].db_id))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(len(messages), 0)

    def test_guild_unverified_reminder_messages_are_deleted_correctly(self):
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(1234, "Test1", 60))
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(2345, "Test2", 120))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(len(messages), 2)
        asyncio.run(self.unverified_reminder_message_service.delete_guild_reminder_messages(1234))
        messages = asyncio.run(self.unverified_reminder_message_service.get_all_unverified_reminder_messages())
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Test2")
