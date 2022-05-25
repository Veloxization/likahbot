import unittest
import os
from dao.unverified_reminder_messages_dao import UnverifiedReminderMessagesDAO

class TestUnverifiedReminderMessagesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.unverified_reminder_messages_dao = UnverifiedReminderMessagesDAO(self.db_addr)

    def tearDown(self):
        self.unverified_reminder_messages_dao.clear_unverified_reminder_messages_table()

    def test_guild_unverified_messages_are_added_correctly(self):
        messages = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        self.assertEqual(len(messages), 0)
        self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(1234, "Test", 0)
        messages = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        self.assertEqual(len(messages), 1)

    def test_guild_unverified_messages_are_edited_correctly(self):
        self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(1234, "Test", 0)
        message = self.unverified_reminder_messages_dao.get_guild_unverified_reminder_messages(1234)[0]
        self.assertEqual(message["message"], "Test")
        self.assertEqual(message["timedelta"], 0)
        self.unverified_reminder_messages_dao.edit_guild_unverified_message(message["id"], "Testing", 5)
        message = self.unverified_reminder_messages_dao.get_guild_unverified_reminder_messages(1234)[0]
        self.assertEqual(message["message"], "Testing")
        self.assertEqual(message["timedelta"], 5)

    def test_unverified_messages_are_deleted_correctly(self):
        self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(1234, "Test", 0)
        messages = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        self.assertEqual(len(messages), 1)
        self.unverified_reminder_messages_dao.delete_unverified_reminder_message(messages[0]["id"])
        messages = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        self.assertEqual(len(messages), 0)

    def test_guild_unverified_messages_are_deleted_correctly(self):
        self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(1234, "Test", 0)
        self.unverified_reminder_messages_dao.add_guild_unverified_reminder_message(2345, "Test", 0)
        messages = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        self.assertEqual(len(messages), 2)
        self.unverified_reminder_messages_dao.delete_guild_reminder_messages(1234)
        messages = self.unverified_reminder_messages_dao.get_all_unverified_reminder_messages()
        self.assertEqual(len(messages), 1)
