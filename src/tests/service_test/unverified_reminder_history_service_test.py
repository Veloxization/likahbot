import asyncio
import unittest
import os
from services.unverified_reminder_history_service import UnverifiedReminderHistoryService
from services.unverified_reminder_message_service import UnverifiedReminderMessageService

class TestUnverifiedReminderHistoryService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.unverified_reminder_history_service = UnverifiedReminderHistoryService(db_address)
        self.unverified_reminder_message_service = UnverifiedReminderMessageService(db_address)
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(9876, "Test1", 60))
        asyncio.run(self.unverified_reminder_message_service.add_guild_unverified_reminder_message(8765, "Test2", 120))
        self.message1 = asyncio.run(self.unverified_reminder_message_service.get_guild_unverified_reminder_messages(9876))[0]
        self.message2 = asyncio.run(self.unverified_reminder_message_service.get_guild_unverified_reminder_messages(8765))[0]

    def tearDown(self):
        asyncio.run(self.unverified_reminder_history_service.clear_unverified_reminder_history())
        asyncio.run(self.unverified_reminder_message_service.clear_unverified_reminder_messages())

    def test_member_reminder_history_is_found_correctly(self):
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(1234, self.message1.db_id))
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(2345, self.message1.db_id))
        history = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 9876))
        self.assertEqual(len(history), 1)

    def test_member_reminder_history_is_deleted_correctly(self):
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(1234, self.message1.db_id))
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(1234, self.message2.db_id))
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(2345, self.message1.db_id))
        history1 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 9876))
        history2 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 8765))
        history3 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(2345, 9876))
        self.assertEqual(len(history1), 1)
        self.assertEqual(len(history2), 1)
        self.assertEqual(len(history3), 1)
        asyncio.run(self.unverified_reminder_history_service.delete_member_reminder_history(1234, 9876))
        history1 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 9876))
        history2 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 8765))
        history3 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(2345, 9876))
        self.assertEqual(len(history1), 0)
        self.assertEqual(len(history2), 1)
        self.assertEqual(len(history3), 1)

    def test_guild_reminder_history_is_deleted_correctly(self):
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(1234, self.message1.db_id))
        asyncio.run(self.unverified_reminder_history_service.add_to_member_reminder_history(1234, self.message2.db_id))
        history1 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 9876))
        history2 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 8765))
        self.assertEqual(len(history1), 1)
        self.assertEqual(len(history2), 1)
        asyncio.run(self.unverified_reminder_history_service.delete_guild_reminder_history(9876))
        history1 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 9876))
        history2 = asyncio.run(self.unverified_reminder_history_service.get_member_reminder_history(1234, 8765))
        self.assertEqual(len(history1), 0)
        self.assertEqual(len(history2), 1)
