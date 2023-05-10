import asyncio
import unittest
import os
from dao.unverified_reminder_history_dao import UnverifiedReminderHistoryDAO
from dao.unverified_reminder_messages_dao import UnverifiedReminderMessagesDAO

class TestUnverifiedReminderHistoryDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.unverified_reminder_history_dao = UnverifiedReminderHistoryDAO(self.db_addr)
        self.unverified_reminder_messages_dao = UnverifiedReminderMessagesDAO(self.db_addr)
        asyncio.run(self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(1234, "Test", 0))
        self.message_id = asyncio.run(self.unverified_reminder_messages_dao.get_guild_unverified_reminder_messages(1234))[0]["id"]
        asyncio.run(self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(2345, "Test", 0))
        self.message_id2 = asyncio.run(self.unverified_reminder_messages_dao.get_guild_unverified_reminder_messages(2345))[0]["id"]

    def tearDown(self):
        asyncio.run(self.unverified_reminder_history_dao.clear_unverified_reminder_history_table())
        asyncio.run(self.unverified_reminder_messages_dao.clear_unverified_reminder_messages_table())

    def test_member_reminder_history_is_added_to_correctly(self):
        reminder_history = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 1234))
        self.assertEqual(len(reminder_history), 0)
        asyncio.run(self.unverified_reminder_history_dao.add_to_member_reminder_history(9876, self.message_id))
        reminder_history = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 1234))
        self.assertEqual(len(reminder_history), 1)

    def test_member_reminder_history_is_deleted_correctly(self):
        asyncio.run(self.unverified_reminder_history_dao.add_to_member_reminder_history(9876, self.message_id))
        asyncio.run(self.unverified_reminder_history_dao.add_to_member_reminder_history(8765, self.message_id))
        reminder_history1 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 1234))
        reminder_history2 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(8765, 1234))
        self.assertEqual(len(reminder_history1), 1)
        self.assertEqual(len(reminder_history2), 1)
        asyncio.run(self.unverified_reminder_history_dao.delete_member_reminder_history(9876, 1234))
        reminder_history1 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 1234))
        reminder_history2 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(8765, 1234))
        self.assertEqual(len(reminder_history1), 0)
        self.assertEqual(len(reminder_history2), 1)

    def test_guild_reminder_history_is_deleted_correctly(self):
        asyncio.run(self.unverified_reminder_history_dao.add_to_member_reminder_history(9876, self.message_id))
        asyncio.run(self.unverified_reminder_history_dao.add_to_member_reminder_history(9876, self.message_id2))
        reminder_history1 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 1234))
        reminder_history2 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 2345))
        self.assertEqual(len(reminder_history1), 1)
        self.assertEqual(len(reminder_history2), 1)
        asyncio.run(self.unverified_reminder_history_dao.delete_guild_reminder_history(1234))
        reminder_history1 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 1234))
        reminder_history2 = asyncio.run(self.unverified_reminder_history_dao.get_member_reminder_history(9876, 2345))
        self.assertEqual(len(reminder_history1), 0)
        self.assertEqual(len(reminder_history2), 1)
