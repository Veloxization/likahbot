import asyncio
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
        asyncio.run(self.settings_dao.clear_settings_table())
        self.setting_id1 = asyncio.run(self.settings_dao.add_setting("test", "test1"))["id"]
        self.setting_id2 = asyncio.run(self.settings_dao.add_setting("testing", "test0"))["id"]

    def tearDown(self):
        asyncio.run(self.guild_settings_dao.clear_guild_settings_table())
        asyncio.run(self.settings_dao.clear_settings_table())

    def test_guild_setting_is_added_correctly_by_setting_id(self):
        id_row = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row["id"]))
        self.assertEqual(row["setting_value"], "test2")

    def test_guild_setting_is_added_correctly_by_setting_name(self):
        id_row = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_name(1234, "test", "test2"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row["id"]))
        self.assertEqual(row["setting_value"], "test2")

    def test_guild_setting_is_found_correctly_by_setting_id(self):
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_setting_id(1234, self.setting_id1))
        self.assertEqual(row["setting_value"], "test2")

    def test_guild_setting_returns_the_default_if_not_set_when_searching_by_id(self):
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_setting_id(1234, self.setting_id1))
        self.assertEqual(row["setting_value"], "test1")

    def test_guild_setting_returns_the_default_if_not_set_when_searching_by_name(self):
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_name(1234, "test"))
        self.assertEqual(row["setting_value"], "test1")

    def test_guild_setting_is_edited_correctly_by_id(self):
        id_row = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.edit_guild_setting_by_id(id_row["id"], "test3"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row["id"]))
        self.assertEqual(row["setting_value"], "test3")

    def test_guild_setting_is_edited_correctly_by_setting_id(self):
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.edit_guild_setting_by_setting_id(1234, self.setting_id1, "test3"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_setting_id(1234, self.setting_id1))
        self.assertEqual(row["setting_value"], "test3")

    def test_guild_setting_is_edited_correctly_by_setting_name(self):
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_name(1234, "test", "test2"))
        asyncio.run(self.guild_settings_dao.edit_guild_setting_by_setting_name(1234, "test", "test3"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_name(1234, "test"))
        self.assertEqual(row["setting_value"], "test3")

    def test_guild_settings_are_deleted_correctly_by_id(self):
        id_row = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.delete_guild_setting_by_id(id_row["id"]))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row["id"]))
        self.assertIsNone(row)

    def test_guild_settings_are_deleted_correctly_by_setting_id(self):
        id_row = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.delete_guild_setting_by_setting_id(1234, self.setting_id1))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row["id"]))
        self.assertIsNone(row)

    def test_guild_settings_are_deleted_correctly_by_setting_name(self):
        id_row = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.delete_guild_setting_by_setting_name(1234, "test"))
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row["id"]))
        self.assertIsNone(row)

    def test_all_guild_settings_of_a_specific_guild_are_deleted_correctly(self):
        id_row1 = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        id_row2 = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(2345, self.setting_id1, "test3"))
        asyncio.run(self.guild_settings_dao.delete_guild_settings(1234))
        row1 = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row1["id"]))
        row2 = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row2["id"]))
        self.assertIsNone(row1)
        self.assertIsNotNone(row2)
