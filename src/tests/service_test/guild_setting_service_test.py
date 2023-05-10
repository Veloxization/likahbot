import asyncio
import unittest
import os
from services.setting_service import SettingService
from services.guild_setting_service import GuildSettingService

class TestGuildSettingService(unittest.TestCase):
    def setUp(self):
        db_address = "database/test_db.db"
        os.popen(f"sqlite3 {db_address} < database/schema.sql")
        self.guild_setting_service = GuildSettingService(db_address)
        self.setting_service = SettingService(db_address)
        self.setting_id = asyncio.run(self.setting_service.add_setting("test", "testing"))
        self.setting = asyncio.run(self.setting_service.get_setting_default_value_by_id(self.setting_id))

    def tearDown(self):
        asyncio.run(self.guild_setting_service.clear_guild_settings())
        asyncio.run(self.setting_service.clear_settings())

    def test_guild_setting_is_found_correctly_by_id(self):
        guild_setting_id = asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_id(guild_setting_id))
        self.assertEqual(guild_setting.value, "testing1")

    def test_guild_setting_is_found_correctly_by_setting_name(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertEqual(guild_setting.value, "testing1")

    def test_guild_setting_is_default_when_searching_by_name_and_setting_not_used_for_guild(self):
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertEqual(guild_setting.value, "testing")

    def test_guild_setting_is_found_correctly_by_setting_id(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_setting_id(1234, self.setting_id))
        self.assertEqual(guild_setting.value, "testing1")

    def test_guild_setting_is_default_when_searching_by_setting_id_and_setting_not_used_for_guild(self):
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_setting_id(1234, self.setting_id))
        self.assertEqual(guild_setting.value, "testing")

    def test_guild_setting_is_added_correctly_by_setting_id(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_id(1234, self.setting_id, "testing1"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_setting_id(1234, self.setting_id))
        self.assertEqual(guild_setting.value, "testing1")

    def test_guild_setting_is_edited_correctly_by_id(self):
        guild_setting_id = asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.edit_guild_setting_by_id(guild_setting_id, "testing2"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_id(guild_setting_id))
        self.assertEqual(guild_setting.value, "testing2")

    def test_guild_setting_is_edited_correctly_by_setting_id(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.edit_guild_setting_by_setting_id(1234, self.setting_id, "testing2"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertEqual(guild_setting.value, "testing2")

    def test_guild_setting_is_edited_correctly_by_setting_name(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.edit_guild_setting_by_setting_name(1234, "test", "testing2"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertEqual(guild_setting.value, "testing2")

    def test_editing_guild_setting_of_one_guild_does_not_affect_guild_setting_of_another_guild(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(2345, "test", "testing1"))
        asyncio.run(self.guild_setting_service.edit_guild_setting_by_setting_name(1234, "test", "testing2"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(2345, "test"))
        self.assertNotEqual(guild_setting.value, "testing2")

    def test_guild_setting_is_deleted_correctly_by_id(self):
        guild_setting_id = asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.delete_guild_setting_by_id(guild_setting_id))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertIsNone(guild_setting.db_id)

    def test_guild_setting_is_deleted_correctly_by_setting_id(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.delete_guild_setting_by_setting_id(1234, self.setting_id))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertIsNone(guild_setting.db_id)

    def test_guild_setting_is_deleted_correctly_by_setting_name(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.delete_guild_setting_by_setting_name(1234, "test"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        self.assertIsNone(guild_setting.db_id)

    def test_deleting_guild_setting_of_one_guild_does_not_affect_guild_setting_of_another_guild(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(2345, "test", "testing1"))
        asyncio.run(self.guild_setting_service.delete_guild_setting_by_setting_name(1234, "test"))
        guild_setting = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(2345, "test"))
        self.assertIsNotNone(guild_setting.db_id)

    def test_all_settings_associated_with_a_given_guild_are_deleted_correctly(self):
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(1234, "test", "testing1"))
        asyncio.run(self.guild_setting_service.add_guild_setting_by_setting_name(2345, "test", "testing2"))
        asyncio.run(self.guild_setting_service.delete_guild_settings(1234))
        guild_setting1 = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(1234, "test"))
        guild_setting2 = asyncio.run(self.guild_setting_service.get_guild_setting_value_by_name(2345, "test"))
        self.assertIsNone(guild_setting1.db_id)
        self.assertEqual(guild_setting2.value, "testing2")
