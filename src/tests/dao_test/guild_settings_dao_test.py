import unittest
import os
from dao.guild_settings_dao import GuildSettingsDAO
from dao.settings_dao import SettingsDAO

class TestGuildSettingsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.guild_settings_dao = GuildSettingsDAO(self.db_addr)
        self.settings_dao = SettingsDAO(self.db_addr)
        self.settings_dao.clear_settings_table()
        self.setting_id1 = self.settings_dao.add_setting("test", "test1")["id"]
        self.setting_id2 = self.settings_dao.add_setting("testing", "test0")["id"]

    def tearDown(self):
        self.guild_settings_dao.clear_guild_settings_table()
        self.settings_dao.clear_settings_table()

    def test_guild_setting_is_added_correctly_by_setting_id(self):
        id_row = self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        row = self.guild_settings_dao.get_guild_setting_status_by_id(id_row["id"])
        self.assertEqual(row["setting_status"], "test2")

    def test_guild_setting_is_added_correctly_by_setting_name(self):
        id_row = self.guild_settings_dao.add_guild_setting_by_setting_name(1234, "test", "test2")
        row = self.guild_settings_dao.get_guild_setting_status_by_id(id_row["id"])
        self.assertEqual(row["setting_status"], "test2")

    def test_guild_setting_is_found_correctly_by_setting_id(self):
        self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        row = self.guild_settings_dao.get_guild_setting_status_by_setting_id(1234, self.setting_id1)
        self.assertEqual(row["setting_status"], "test2")

    def test_guild_setting_returns_the_default_if_not_set_when_searching_by_id(self):
        row = self.guild_settings_dao.get_guild_setting_status_by_setting_id(1234, self.setting_id1)
        self.assertEqual(row["setting_status"], "test1")

    def test_guild_setting_returns_the_default_if_not_set_when_searching_by_name(self):
        row = self.guild_settings_dao.get_guild_setting_status_by_name(1234, "test")
        self.assertEqual(row["setting_status"], "test1")

    def test_guild_setting_is_edited_correctly_by_id(self):
        id_row = self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        self.guild_settings_dao.edit_guild_setting_by_id(id_row["id"], "test3")
        row = self.guild_settings_dao.get_guild_setting_status_by_id(id_row["id"])
        self.assertEqual(row["setting_status"], "test3")

    def test_guild_setting_is_edited_correctly_by_setting_id(self):
        self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        self.guild_settings_dao.edit_guild_setting_by_setting_id(1234, self.setting_id1, "test3")
        row = self.guild_settings_dao.get_guild_setting_status_by_setting_id(1234, self.setting_id1)
        self.assertEqual(row["setting_status"], "test3")

    def test_guild_setting_is_edited_correctly_by_setting_name(self):
        self.guild_settings_dao.add_guild_setting_by_setting_name(1234, "test", "test2")
        self.guild_settings_dao.edit_guild_setting_by_setting_name(1234, "test", "test3")
        row = self.guild_settings_dao.get_guild_setting_status_by_name(1234, "test")
        self.assertEqual(row["setting_status"], "test3")

    def test_guild_settings_are_deleted_correctly_by_id(self):
        id_row = self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        self.guild_settings_dao.delete_guild_setting_by_id(id_row["id"])
        row = self.guild_settings_dao.get_guild_setting_status_by_id(id_row["id"])
        self.assertIsNone(row)

    def test_guild_settings_are_deleted_correctly_by_setting_id(self):
        id_row = self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        self.guild_settings_dao.delete_guild_setting_by_setting_id(1234, self.setting_id1)
        row = self.guild_settings_dao.get_guild_setting_status_by_id(id_row["id"])
        self.assertIsNone(row)

    def test_guild_settings_are_deleted_correctly_by_setting_name(self):
        id_row = self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        self.guild_settings_dao.delete_guild_setting_by_setting_name(1234, "test")
        row = self.guild_settings_dao.get_guild_setting_status_by_id(id_row["id"])
        self.assertIsNone(row)

    def test_all_guild_settings_of_a_specific_guild_are_deleted_correctly(self):
        id_row1 = self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2")
        id_row2 = self.guild_settings_dao.add_guild_setting_by_setting_id(2345, self.setting_id1, "test3")
        self.guild_settings_dao.delete_guild_settings(1234)
        row1 = self.guild_settings_dao.get_guild_setting_status_by_id(id_row1["id"])
        row2 = self.guild_settings_dao.get_guild_setting_status_by_id(id_row2["id"])
        self.assertIsNone(row1)
        self.assertIsNotNone(row2)
