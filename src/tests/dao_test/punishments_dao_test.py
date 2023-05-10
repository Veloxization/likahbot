import asyncio
import unittest
import os
from dao.punishments_dao import PunishmentsDAO

class TestPunishmentsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.punishments_dao = PunishmentsDAO(self.db_addr)

    def tearDown(self):
        asyncio.run(self.punishments_dao.clear_punishments_table())

    def test_punishments_are_added_correctly(self):
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 0)
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 1)

    def test_added_punishments_are_returned_correctly(self):
        punishment_id = asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))["id"]
        punishment = asyncio.run(self.punishments_dao.get_punishment_by_id(punishment_id))
        self.assertEqual(punishment["user_id"], 1234)
        self.assertEqual(punishment["issuer_id"], 2345)
        self.assertEqual(punishment["guild_id"], 9876)

    def test_censored_punishments_are_found_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        asyncio.run(self.punishments_dao.delete_user_id_from_punishments(1234))
        punishments = asyncio.run(self.punishments_dao.get_censored_punishments(9876))
        self.assertEqual(len(punishments), 1)
        self.assertEqual(punishments[0]["user_id"], 0)

    def test_punishments_are_marked_deleted_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        self.assertFalse(punishments[0]["deleted"])
        asyncio.run(self.punishments_dao.mark_deleted(punishments[0]["id"]))
        punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        self.assertTrue(punishments[0]["deleted"])

    def test_punishments_marked_deleted_are_unmarked_deleted_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876, deleted=True))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 0)
        all_punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        asyncio.run(self.punishments_dao.unmark_deleted(all_punishments[0]["id"]))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 1)

    def test_deleted_punishments_are_found_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876, deleted=True))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 0)
        punishments = asyncio.run(self.punishments_dao.get_deleted_punishments(1234, 9876))
        self.assertEqual(len(punishments), 1)

    def test_punishment_reasons_are_edited_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876, reason="Test1"))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(punishments[0]["reason"], "Test1")
        asyncio.run(self.punishments_dao.edit_punishment_reason(punishments[0]["id"], "Test2"))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(punishments[0]["reason"], "Test2")

    def test_punishments_are_deleted_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 1)
        asyncio.run(self.punishments_dao.delete_punishment(punishments[0]["id"]))
        punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 0)

    def test_punishments_marked_deleted_are_not_returned(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 1)
        asyncio.run(self.punishments_dao.mark_deleted(punishments[0]["id"]))
        punishments = asyncio.run(self.punishments_dao.get_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 0)

    def test_punishments_for_user_are_censored_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        asyncio.run(self.punishments_dao.add_punishment(1234, 3456, 8765))
        asyncio.run(self.punishments_dao.delete_user_id_from_punishments(1234))
        punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        self.assertEqual(len(punishments), 0)
        punishments = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 8765))
        self.assertEqual(len(punishments), 0)

    def test_guild_punishments_are_cleared_correctly(self):
        asyncio.run(self.punishments_dao.add_punishment(1234, 2345, 9876))
        asyncio.run(self.punishments_dao.add_punishment(1234, 3456, 8765))
        punishments1 = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        punishments2 = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 8765))
        self.assertEqual(len(punishments1), 1)
        self.assertEqual(len(punishments2), 1)
        asyncio.run(self.punishments_dao.delete_guild_punishments(9876))
        punishments1 = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 9876))
        punishments2 = asyncio.run(self.punishments_dao.get_all_user_punishments(1234, 8765))
        self.assertEqual(len(punishments1), 0)
        self.assertEqual(len(punishments2), 1)
