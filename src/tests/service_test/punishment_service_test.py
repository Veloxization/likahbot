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

    def test_added_punishments_are_returned_correctly(self):
        punishment = self.punishment_service.add_punishment(1234, 3456, 9876)
        self.assertEqual(punishment.user_id, 1234)
        self.assertEqual(punishment.issuer_id, 3456)
        self.assertEqual(punishment.guild_id, 9876)

    def test_user_punishments_are_found_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876)
        self.punishment_service.add_punishment(2345, 3456, 9876)
        punishments = self.punishment_service.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)
        self.assertEqual(punishments[0].user_id, 1234)

    def test_punishments_are_found_correctly_by_id(self):
        punishment1 = self.punishment_service.add_punishment(1234, 3456, 9876)
        punishment2 = self.punishment_service.get_punishment_by_id(punishment1.db_id)
        self.assertEqual(punishment1.db_id, punishment2.db_id)
        self.assertEqual(punishment1.issuer_id, punishment2.issuer_id)
        self.assertEqual(punishment1.user_id, punishment2.user_id)
        self.assertEqual(punishment1.guild_id, punishment2.guild_id)

    def test_user_punishments_are_marked_deleted_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876)
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertFalse(punishments[0].deleted)
        self.punishment_service.mark_deleted(punishments[0].db_id)
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertTrue(punishments[0].deleted)

    def test_deleted_punishments_are_marked_undeleted_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876, deleted=True)
        punishments = self.punishment_service.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 0)
        all_punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.punishment_service.unmark_deleted(all_punishments[0].db_id)
        punishments = self.punishment_service.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)

    def test_punishment_reasons_are_edited_correctly(self):
        self.punishment_service.add_punishment(1234, 3456, 9876, reason="Test1")
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertEqual(punishments[0].reason, "Test1")
        self.punishment_service.edit_punishment_reason(punishments[0].db_id, "Test2")
        punishments = self.punishment_service.get_all_user_punishments(1234, 9876)
        self.assertEqual(punishments[0].reason, "Test2")

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
