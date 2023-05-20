import asyncio
import unittest
import os
from dao.utility_channels_dao import UtilityChannelsDAO

class TestUtilityChannelsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.utility_channels_dao = UtilityChannelsDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.utility_channels_dao.clear_utility_channels_table())

    def test_utility_channels_are_added_correctly(self):
        channels = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(9876))
        self.assertEqual(len(channels), 0)
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST"))
        channels = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(9876))
        self.assertEqual(len(channels), 1)

    def test_utility_channels_are_deleted_correctly(self):
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST"))
        channels = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(9876))
        self.assertEqual(len(channels), 1)
        asyncio.run(self.utility_channels_dao.delete_utility_channel(1234, 9876))
        channels = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(9876))
        self.assertEqual(len(channels), 0)

    def test_certain_utilities_are_removed_from_channels_correctly(self):
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST1"))
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST2"))
        channels = asyncio.run(self.utility_channels_dao.get_guild_utility_channel_by_id(9876, 1234))
        self.assertEqual(len(channels), 2)
        asyncio.run(self.utility_channels_dao.delete_utility_from_channel(1234, 9876, "TEST1"))
        channels = asyncio.run(self.utility_channels_dao.get_guild_utility_channel_by_id(9876, 1234))
        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0]["channel_purpose"], "TEST2")

    def test_guild_utility_channels_are_deleted_correctly(self):
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST"))
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(2345, 8765, "TEST"))
        channels1 = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(9876))
        channels2 = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(8765))
        self.assertEqual(len(channels1), 1)
        self.assertEqual(len(channels2), 1)
        asyncio.run(self.utility_channels_dao.delete_guild_utility_channels(9876))
        channels1 = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(9876))
        channels2 = asyncio.run(self.utility_channels_dao.get_all_guild_utility_channels(8765))
        self.assertEqual(len(channels1), 0)
        self.assertEqual(len(channels2), 1)

    def test_utility_channels_by_purpose_are_returned_correctly(self):
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST1"))
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(2345, 9876, "TEST1"))
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(3456, 9876, "TEST2"))
        channels1 = asyncio.run(self.utility_channels_dao.get_guild_utility_channel_by_purpose(9876, "TEST1"))
        channels2 = asyncio.run(self.utility_channels_dao.get_guild_utility_channel_by_purpose(9876, "TEST2"))
        self.assertEqual(len(channels1), 2)
        self.assertEqual(len(channels2), 1)

    def test_utility_channels_by_id_are_returned_correctly(self):
        asyncio.run(self.utility_channels_dao.create_guild_utility_channel(1234, 9876, "TEST"))
        channels = asyncio.run(self.utility_channels_dao.get_guild_utility_channel_by_id(9876, 1234))
        self.assertEqual(channels[0]["channel_id"], 1234)
        self.assertEqual(channels[0]["guild_id"], 9876)
        self.assertEqual(channels[0]["channel_purpose"], "TEST")
