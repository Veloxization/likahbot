import unittest
import os
from dao.passphrases_dao import PassphrasesDAO

class TestPassphrasesDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.passphrases_dao = PassphrasesDAO(self.db_addr)

    def tearDown(self):
        self.passphrases_dao.clear_passphrases_table()

    def test_passphrases_are_added_correctly(self):
        self.passphrases_dao.add_passphrase(1234, "TEST")
        passphrases = self.passphrases_dao.get_all_guild_passphrases(1234)
        self.assertEqual(len(passphrases), 1)
        self.passphrases_dao.add_passphrase(1234, "TEST 2")
        passphrases = self.passphrases_dao.get_all_guild_passphrases(1234)
        self.assertEqual(len(passphrases), 2)

    def test_passphrases_are_deleted_correctly(self):
        self.passphrases_dao.add_passphrase(1234, "TEST")
        passphrases = self.passphrases_dao.get_all_guild_passphrases(1234)
        self.assertEqual(len(passphrases), 1)
        self.passphrases_dao.delete_passphrase(passphrases[0]["id"])
        passphrases = self.passphrases_dao.get_all_guild_passphrases(1234)
        self.assertEqual(len(passphrases), 0)

    def test_guild_passphrases_are_cleared_correctly(self):
        self.passphrases_dao.add_passphrase(1234, "TEST")
        self.passphrases_dao.add_passphrase(2345, "TEST")
        passphrases1 = self.passphrases_dao.get_all_guild_passphrases(1234)
        passphrases2 = self.passphrases_dao.get_all_guild_passphrases(2345)
        self.assertEqual(len(passphrases1), 1)
        self.assertEqual(len(passphrases2), 1)
        self.passphrases_dao.delete_guild_passphrases(1234)
        passphrases1 = self.passphrases_dao.get_all_guild_passphrases(1234)
        passphrases2 = self.passphrases_dao.get_all_guild_passphrases(2345)
        self.assertEqual(len(passphrases1), 0)
        self.assertEqual(len(passphrases2), 1)
