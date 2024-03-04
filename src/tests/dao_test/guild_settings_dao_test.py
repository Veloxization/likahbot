import asyncio
import unittest
import os
from dao.guild_settings_dao import GuildSettingsDAO
from dao.settings_dao import SettingsDAO

class TestGuildSettingsDAO(unittest.TestCase):
    def setUp(self):
        self.db_addr = "database/test_db.db"
        os.popen(f"sqlite3 {self.db_addr} < database/test_schema.sql")
        self.guild_settings_dao = GuildSettingsDAO(self.db_addr)
        self.settings_dao = SettingsDAO(self.db_addr)
        asyncio.run(self.settings_dao.clear_settings_table())
        self.setting_id1 = asyncio.run(self.settings_dao.add_setting("test", "test1"))["id"]
        self.setting_id2 = asyncio.run(self.settings_dao.add_setting("testing", "test0"))["id"]

    def tearDown(self):
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
    
    def test_all_guild_settings_of_a_specific_guild_are_found_correctly(self):
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(2345, self.setting_id1, "test3"))
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id2, "test4"))
        rows = asyncio.run(self.guild_settings_dao.get_all_guild_settings(1234))
        self.assertEqual(len(rows), 2)
        self.assertNotEqual(rows[0]["setting_value"], "test3")
        self.assertNotEqual(rows[1]["setting_value"], "test3")

    def test_guild_settings_are_found_correctly_through_search(self):
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id2, "test3"))
        asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(2345, self.setting_id2, "test4"))
        rows = asyncio.run(self.guild_settings_dao.search_guild_settings(1234, "sti"))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["setting_value"], "test3")

    def test_guild_settings_are_initialized_correctly(self):
        rows = asyncio.run(self.guild_settings_dao.initialize_guild_settings(1234))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["id"], self.setting_id1)
        self.assertEqual(rows[1]["id"], self.setting_id2)

    def test_guild_settings_are_initialized_correctly_when_new_settings_are_added(self):
        asyncio.run(self.guild_settings_dao.initialize_guild_settings(1234))
        asyncio.run(self.settings_dao.add_setting("another_test", "test-1"))
        rows = asyncio.run(self.guild_settings_dao.initialize_guild_settings(1234))
        self.assertEqual(len(rows), 1)
        row = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(rows[0]["id"]))
        self.assertEqual(row["setting_value"], "test-1")

    def test_guild_settings_are_correctly_reset_to_default_value(self):
        row1 = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        asyncio.run(self.guild_settings_dao.reset_guild_setting_to_default_value(1234, row1["id"]))
        row2 = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(row1["id"]))
        self.assertEqual(row2["setting_value"], "test1")

    def test_all_guild_settings_are_correctly_reset_to_default_values(self):
        id_row1 = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id1, "test2"))
        id_row2 = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(2345, self.setting_id1, "test3"))
        id_row3 = asyncio.run(self.guild_settings_dao.add_guild_setting_by_setting_id(1234, self.setting_id2, "test4"))
        asyncio.run(self.guild_settings_dao.reset_all_guild_settings_to_default_value(1234))
        row1 = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row1["id"]))
        row2 = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row2["id"]))
        row3 = asyncio.run(self.guild_settings_dao.get_guild_setting_value_by_id(id_row3["id"]))
        self.assertEqual(row1["setting_value"], "test1")
        self.assertEqual(row2["setting_value"], "test3")
        self.assertEqual(row3["setting_value"], "test0")
