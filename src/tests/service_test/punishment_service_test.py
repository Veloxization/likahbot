import unittest
import os
from services.punishment_service import PunishmentService

class TestPunishmentService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.punishment_service = PunishmentService(db_address)

    def tearDown(self):
        self.punishment_service.clear_punishments()

    def test_user_punishments_are_found_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876)
        self.punishment_service.add_punishment(2345, 3456, 9876)
        punishments = self.punishment_service.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)
        self.assertEqual(punishments[0].user_id, 1234)

    def test_user_punishments_are_marked_deleted_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876)
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertFalse(punishments[0].deleted)
        self.punishment_service.mark_deleted(punishments[0].db_id)
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertTrue(punishments[0].deleted)

    def test_deleted_user_punishments_are_not_returned_with_regular_search(self):
        self.punishment_service.add_punishment(1234, 3456, 9876, deleted=True)
        punishments = self.punishment_service.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 0)

    def test_punishments_are_permanently_deleted_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876)
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)
        self.punishment_service.delete_punishment(punishments[0].db_id)
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 0)

    def test_guild_punishments_are_deleted_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876)
        self.punishment_service.add_punishment(1234, 4567, 8765)
        punishments1 = self.punishment_service.get_all_user_punishments(1234, 9876)
        punishments2 = self.punishment_service.get_all_user_punishments(1234, 8765)
        self.assertEqual(len(punishments1), 1)
        self.assertEqual(len(punishments2), 1)
        self.punishment_service.delete_guild_punishments(9876)
        punishments1 = self.punishment_service.get_all_user_punishments(1234, 9876)
        punishments2 = self.punishment_service.get_all_user_punishments(1234, 8765)
        self.assertEqual(len(punishments1), 0)
        self.assertEqual(len(punishments2), 1)
