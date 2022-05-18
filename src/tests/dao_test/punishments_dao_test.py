import unittest
import os
from dao.punishments_dao import PunishmentsDAO

class TestPunishmentsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.punishments_dao = PunishmentsDAO(self.db_addr)

    def tearDown(self):
        self.punishments_dao.clear_punishments_table()

    def test_punishments_are_added_correctly(self):
        punishments = self.punishments_dao.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 0)
        self.punishments_dao.add_punishment(1234, 2345, 9876)
        punishments = self.punishments_dao.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)

    def test_punishments_are_marked_deleted_correctly(self):
        self.punishments_dao.add_punishment(1234, 2345, 9876)
        punishments = self.punishments_dao.get_all_user_punishments(1234, 9876)
        self.assertFalse(punishments[0]["deleted"])
        self.punishments_dao.mark_deleted(punishments[0]["id"])
        punishments = self.punishments_dao.get_all_user_punishments(1234, 9876)
        self.assertTrue(punishments[0]["deleted"])

    def test_punishments_are_deleted_correctly(self):
        self.punishments_dao.add_punishment(1234, 2345, 9876)
        punishments = self.punishments_dao.get_all_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)
        self.punishments_dao.delete_punishment(punishments[0]["id"])
        punishments = self.punishments_dao.get_all_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 0)

    def test_punishments_marked_deleted_are_not_returned(self):
        self.punishments_dao.add_punishment(1234, 2345, 9876)
        punishments = self.punishments_dao.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 1)
        self.punishments_dao.mark_deleted(punishments[0]["id"])
        punishments = self.punishments_dao.get_user_punishments(1234, 9876)
        self.assertEqual(len(punishments), 0)

    def test_guild_punishments_are_cleared_correctly(self):
        self.punishments_dao.add_punishment(1234, 2345, 9876)
        self.punishments_dao.add_punishment(1234, 3456, 8765)
        punishments1 = self.punishments_dao.get_all_user_punishments(1234, 9876)
        punishments2 = self.punishments_dao.get_all_user_punishments(1234, 8765)
        self.assertEqual(len(punishments1), 1)
        self.assertEqual(len(punishments2), 1)
        self.punishments_dao.delete_guild_punishments(9876)
        punishments1 = self.punishments_dao.get_all_user_punishments(1234, 9876)
        punishments2 = self.punishments_dao.get_all_user_punishments(1234, 8765)
        self.assertEqual(len(punishments1), 0)
        self.assertEqual(len(punishments2), 1)
