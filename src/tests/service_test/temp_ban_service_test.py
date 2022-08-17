import unittest
import os
from datetime import datetime, timedelta
from services.temp_ban_service import TempBanService

class TestTempBanService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.temp_ban_service = TempBanService(db_address)
        self.expiration1 = datetime.utcnow() + timedelta(days=1)
        self.expiration2 = datetime.utcnow() + timedelta(days=-1)

    def tearDown(self):
        self.temp_ban_service.clear_temp_bans()

    def test_guild_temp_bans_are_found_correctly(self):
        temp_bans = self.temp_ban_service.get_guild_temp_bans(9876)
        self.assertEqual(len(temp_bans), 0)
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration1)
        temp_bans = self.temp_ban_service.get_guild_temp_bans(9876)
        self.assertEqual(len(temp_bans), 1)

    def test_expired_temp_bans_are_found_correctly(self):
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration2)
        self.temp_ban_service.create_temp_ban(2345, 9876, self.expiration1)
        self.temp_ban_service.create_temp_ban(1234, 8765, self.expiration2)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 2)
        self.assertEqual(temp_bans[0].user_id, temp_bans[1].user_id)

    def test_specific_temp_bans_are_found_correctly(self):
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration1)
        self.temp_ban_service.create_temp_ban(2345, 8765, self.expiration1)
        temp_ban = self.temp_ban_service.get_temp_ban(1234, 9876)
        self.assertEqual(temp_ban.user_id, 1234)
        self.assertEqual(temp_ban.guild_id, 9876)

    def test_temp_bans_are_edited_correctly(self):
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration1)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 0)
        self.temp_ban_service.edit_temp_ban(1234, 9876, self.expiration2)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 1)

    def test_temp_bans_are_deleted_correctly(self):
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration2)
        self.temp_ban_service.create_temp_ban(1234, 8765, self.expiration2)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 2)
        self.temp_ban_service.delete_temp_ban(1234, 9876)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 1)
        self.assertEqual(temp_bans[0].guild_id, 8765)

    def test_user_temp_bans_are_deleted_correctly(self):
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration2)
        self.temp_ban_service.create_temp_ban(2345, 9876, self.expiration2)
        self.temp_ban_service.create_temp_ban(1234, 8765, self.expiration2)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 3)
        self.temp_ban_service.delete_user_temp_bans(1234)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 1)
        self.assertNotEqual(temp_bans[0].user_id, 1234)

    def test_guild_temp_bans_are_deleted_correctly(self):
        self.temp_ban_service.create_temp_ban(1234, 9876, self.expiration2)
        self.temp_ban_service.create_temp_ban(2345, 9876, self.expiration2)
        self.temp_ban_service.create_temp_ban(1234, 8765, self.expiration2)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 3)
        self.temp_ban_service.delete_guild_temp_bans(9876)
        temp_bans = self.temp_ban_service.get_expired_temp_bans()
        self.assertEqual(len(temp_bans), 1)
        self.assertNotEqual(temp_bans[0].guild_id, 9876)
