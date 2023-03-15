import unittest
import os
from dao.settings_dao import SettingsDAO

class TestSettingsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/schema.sql")
        self.settings_dao = SettingsDAO(self.db_addr)
        self.settings_dao.clear_settings_table()

    def tearDown(self):
        self.settings_dao.clear_settings_table()

    def test_settings_are_added_correctly(self):
        row = self.settings_dao.get_setting_default_value("test")
        self.assertIsNone(row)
        self.settings_dao.add_setting("test", "testing")
        row = self.settings_dao.get_setting_default_value("test")
        self.assertEqual(row["setting_value"], "testing")

    def test_settings_are_found_by_id(self):
        id_row = self.settings_dao.add_setting("test", "testing")
        row = self.settings_dao.get_setting_default_value_by_id(id_row["id"])
        self.assertEqual(row["setting_value"], "testing")

    def test_setting_defaults_are_edited_correctly_by_name(self):
        self.settings_dao.add_setting("test", "testing1")
        self.settings_dao.edit_setting_default_by_name("test", "testing2")
        row = self.settings_dao.get_setting_default_value("test")
        self.assertEqual(row["setting_value"], "testing2")

    def test_setting_defaults_are_edited_correctly_by_id(self):
        id_row = self.settings_dao.add_setting("test", "testing1")
        self.settings_dao.edit_setting_default_by_id(id_row["id"], "testing2")
        row = self.settings_dao.get_setting_default_value_by_id(id_row["id"])
        self.assertEqual(row["setting_value"], "testing2")

    def test_settings_are_deleted_correctly_by_name(self):
        self.settings_dao.add_setting("test", "testing")
        self.settings_dao.delete_setting_by_name("test")
        row = self.settings_dao.get_setting_default_value("test")
        self.assertIsNone(row)

    def test_settings_are_deleted_correctly_by_id(self):
        id_row = self.settings_dao.add_setting("test", "testing")
        self.settings_dao.delete_setting_by_id(id_row["id"])
        row = self.settings_dao.get_setting_default_value_by_id(id_row["id"])
        self.assertIsNone(row)
