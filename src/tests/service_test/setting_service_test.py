import asyncio
import unittest
import os
from services.setting_service import SettingService

class TestSettingService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.setting_service = SettingService(db_address)
        asyncio.run(self.setting_service.clear_settings())

    def tearDown(self):
        asyncio.run(self.setting_service.clear_settings())

    def test_setting_default_value_is_found_correctly(self):
        asyncio.run(self.setting_service.add_setting("test", "testing"))
        setting = asyncio.run(self.setting_service.get_setting_default_value("test"))
        self.assertEqual(setting.value, "testing")

    def test_setting_default_value_is_found_correctly_by_id(self):
        setting_id = asyncio.run(self.setting_service.add_setting("test", "testing"))
        setting = asyncio.run(self.setting_service.get_setting_default_value_by_id(setting_id))
        self.assertEqual(setting.value, "testing")

    def test_setting_default_value_is_edited_correctly(self):
        asyncio.run(self.setting_service.add_setting("test", "testing"))
        asyncio.run(self.setting_service.edit_setting_default_by_name("test", "testing2"))
        setting = asyncio.run(self.setting_service.get_setting_default_value("test"))
        self.assertEqual(setting.value, "testing2")

    def test_setting_default_value_is_edited_correctly_by_id(self):
        setting_id = asyncio.run(self.setting_service.add_setting("test", "testing"))
        asyncio.run(self.setting_service.edit_setting_default_by_id(setting_id, "testing2"))
        setting = asyncio.run(self.setting_service.get_setting_default_value_by_id(setting_id))
        self.assertEqual(setting.value, "testing2")

    def test_setting_is_deleted_correctly(self):
        asyncio.run(self.setting_service.add_setting("test", "testing"))
        asyncio.run(self.setting_service.delete_setting_by_name("test"))
        setting = asyncio.run(self.setting_service.get_setting_default_value("test"))
        self.assertIsNone(setting)

    def test_setting_is_deleted_correctly_by_id(self):
        setting_id = asyncio.run(self.setting_service.add_setting("test", "testing"))
        asyncio.run(self.setting_service.delete_setting_by_id(setting_id))
        setting = asyncio.run(self.setting_service.get_setting_default_value_by_id(setting_id))
        self.assertIsNone(setting)
