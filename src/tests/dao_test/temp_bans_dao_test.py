import asyncio
import unittest
import os
from datetime import datetime, timedelta
from dao.temp_bans_dao import TempBansDAO

class TestTempBansDAO(unittest.TestCase):
    def setUp(self):
        db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {db_addr} < database/schema.sql")
        self.temp_bans_dao = TempBansDAO(db_addr)
        self.expiration1 = datetime.utcnow() + timedelta(days=1)
        self.expiration2 = datetime.utcnow() + timedelta(days=-1)

    def tearDown(self):
        asyncio.run(self.temp_bans_dao.clear_temp_bans_table())

    def test_guild_temp_bans_are_found_correctly(self):
        temp_bans = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        self.assertEqual(len(temp_bans), 0)
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(2345, 8765, self.expiration1))
        temp_bans = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        self.assertEqual(len(temp_bans), 1)
        self.assertEqual(temp_bans[0]["user_id"], 1234)

    def test_expired_temp_bans_are_found_correctly(self):
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(2345, 9876, self.expiration2))
        asyncio.run(self.temp_bans_dao.create_temp_ban(3456, 8765, self.expiration2))
        temp_bans = asyncio.run(self.temp_bans_dao.get_expired_temp_bans())
        self.assertEqual(len(temp_bans), 2)
        self.assertNotEqual(temp_bans[0]["user_id"], 1234)
        self.assertNotEqual(temp_bans[1]["user_id"], 1234)

    def test_specific_temp_bans_are_found_correctly(self):
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(2345, 9876, self.expiration1))
        temp_ban = asyncio.run(self.temp_bans_dao.get_temp_ban(1234, 9876))
        self.assertEqual(temp_ban["user_id"], 1234)
        self.assertEqual(temp_ban["guild_id"], 9876)

    def test_temp_bans_are_edited_correctly(self):
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration2))
        temp_bans = asyncio.run(self.temp_bans_dao.get_expired_temp_bans())
        self.assertEqual(len(temp_bans), 1)
        asyncio.run(self.temp_bans_dao.edit_temp_ban(1234, 9876, self.expiration1))
        temp_bans = asyncio.run(self.temp_bans_dao.get_expired_temp_bans())
        self.assertEqual(len(temp_bans), 0)

    def test_temp_bans_are_deleted_correctly(self):
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(2345, 9876, self.expiration1))
        temp_bans = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        self.assertEqual(len(temp_bans), 2)
        asyncio.run(self.temp_bans_dao.delete_temp_ban(1234, 9876))
        temp_bans = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        self.assertEqual(len(temp_bans), 1)

    def test_user_temp_bans_are_deleted_correctly(self):
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(2345, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 8765, self.expiration1))
        temp_bans1 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        temp_bans2 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(8765))
        self.assertEqual(len(temp_bans1), 2)
        self.assertEqual(len(temp_bans2), 1)
        asyncio.run(self.temp_bans_dao.delete_user_temp_bans(1234))
        temp_bans1 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        temp_bans2 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(8765))
        self.assertEqual(len(temp_bans1), 1)
        self.assertEqual(len(temp_bans2), 0)

    def test_guild_temp_bans_are_deleted_correctly(self):
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 9876, self.expiration1))
        asyncio.run(self.temp_bans_dao.create_temp_ban(1234, 8765, self.expiration1))
        temp_bans1 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        temp_bans2 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(8765))
        self.assertEqual(len(temp_bans1), 1)
        self.assertEqual(len(temp_bans2), 1)
        asyncio.run(self.temp_bans_dao.delete_guild_temp_bans(9876))
        temp_bans1 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(9876))
        temp_bans2 = asyncio.run(self.temp_bans_dao.get_guild_temp_bans(8765))
        self.assertEqual(len(temp_bans1), 0)
        self.assertEqual(len(temp_bans2), 1)
