import unittest
import os
from services.utility_channel_service import UtilityChannelService

class TestUtilityChannelService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.utility_channel_service = UtilityChannelService(db_address)

    def tearDown(self):
        self.utility_channel_service.clear_utility_channels()

    def test_guild_utility_channels_by_purpose_are_found_correctly(self):
        self.utility_channel_service.create_guild_utility_channel(1234, 9876, "test")
        channels = self.utility_channel_service.get_guild_utility_channel_by_purpose(9876, "test")
        self.assertEqual(len(channels), 1)

    def test_guild_utility_channels_are_found_correctly(self):
        self.utility_channel_service.create_guild_utility_channel(1234, 9876, "test1")
        self.utility_channel_service.create_guild_utility_channel(2345, 8765, "test2")
        channels = self.utility_channel_service.get_all_guild_utility_channels(9876)
        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0].channel_id, 1234)

    def test_guild_utility_channels_by_id_are_found_correctly(self):
        self.utility_channel_service.create_guild_utility_channel(1234, 9876, "test1")
        self.utility_channel_service.create_guild_utility_channel(2345, 9876, "test2")
        channels = self.utility_channel_service.get_guild_utility_channel_by_id(9876, 1234)
        self.assertEqual(channels[0].channel_purpose, "test1")

    def test_utility_channel_is_deleted_correctly(self):
        self.utility_channel_service.create_guild_utility_channel(1234, 9876, "test")
        channels = self.utility_channel_service.get_all_guild_utility_channels(9876)
        self.assertEqual(len(channels), 1)
        self.utility_channel_service.delete_utility_channel(1234, 9876)
        channels = self.utility_channel_service.get_all_guild_utility_channels(9876)
        self.assertEqual(len(channels), 0)

    def test_guild_utility_channels_are_deleted_correctly(self):
        self.utility_channel_service.create_guild_utility_channel(1234, 9876, "test1")
        self.utility_channel_service.create_guild_utility_channel(2345, 8765, "test2")
        channels1 = self.utility_channel_service.get_all_guild_utility_channels(9876)
        channels2 = self.utility_channel_service.get_all_guild_utility_channels(8765)
        self.assertEqual(len(channels1), 1)
        self.assertEqual(len(channels2), 1)
        self.utility_channel_service.delete_guild_utility_channels(9876)
        channels1 = self.utility_channel_service.get_all_guild_utility_channels(9876)
        channels2 = self.utility_channel_service.get_all_guild_utility_channels(8765)
        self.assertEqual(len(channels1), 0)
        self.assertEqual(len(channels2), 1)
