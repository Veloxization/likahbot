import asyncio
import unittest
import os
from dao.settings_dao import SettingsDAO

class TestSettingsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.settings_dao = SettingsDAO(self.db_addr)
        asyncio.run(self.settings_dao.clear_settings_table())

    def tearDown(self):
        asyncio.run(self.settings_dao.clear_settings_table())

    def test_settings_are_added_correctly(self):
        row = asyncio.run(self.settings_dao.get_setting_default_value("test"))
        self.assertIsNone(row)
        asyncio.run(self.settings_dao.add_setting("test", "testing"))
        row = asyncio.run(self.settings_dao.get_setting_default_value("test"))
        self.assertEqual(row["setting_value"], "testing")

    def test_settings_are_found_by_id(self):
        id_row = asyncio.run(self.settings_dao.add_setting("test", "testing"))
        row = asyncio.run(self.settings_dao.get_setting_default_value_by_id(id_row["id"]))
        self.assertEqual(row["setting_value"], "testing")

    def test_setting_defaults_are_edited_correctly_by_name(self):
        asyncio.run(self.settings_dao.add_setting("test", "testing1"))
        asyncio.run(self.settings_dao.edit_setting_default_by_name("test", "testing2"))
        row = asyncio.run(self.settings_dao.get_setting_default_value("test"))
        self.assertEqual(row["setting_value"], "testing2")

    def test_setting_defaults_are_edited_correctly_by_id(self):
        id_row = asyncio.run(self.settings_dao.add_setting("test", "testing1"))
        asyncio.run(self.settings_dao.edit_setting_default_by_id(id_row["id"], "testing2"))
        row = asyncio.run(self.settings_dao.get_setting_default_value_by_id(id_row["id"]))
        self.assertEqual(row["setting_value"], "testing2")

    def test_settings_are_deleted_correctly_by_name(self):
        asyncio.run(self.settings_dao.add_setting("test", "testing"))
        asyncio.run(self.settings_dao.delete_setting_by_name("test"))
        row = asyncio.run(self.settings_dao.get_setting_default_value("test"))
        self.assertIsNone(row)

    def test_settings_are_deleted_correctly_by_id(self):
        id_row = asyncio.run(self.settings_dao.add_setting("test", "testing"))
        asyncio.run(self.settings_dao.delete_setting_by_id(id_row["id"]))
        row = asyncio.run(self.settings_dao.get_setting_default_value_by_id(id_row["id"]))
        self.assertIsNone(row)
